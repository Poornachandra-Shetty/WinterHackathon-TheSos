"""
Analysis API Routes - WITHOUT SURVEY
Handles cognitive tests, speech analysis, and Google Docs report generation
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
import os
import uuid
import threading
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.model import predict_cognitive_risk, predict_speech_risk
from ai.audio_features import extract_audio_features, features_to_array
from ai.risk_score import (
    calculate_risk_score,
    determine_risk_category,
    generate_recommendations,
    get_risk_insights
)

# Import Google Docs report generator
try:
    from generate_report import generate_data
    GDOCS_AVAILABLE = True
    print("✓ Google Docs report generation enabled")
except ImportError:
    GDOCS_AVAILABLE = False
    print("⚠ Google Docs report generation not available (generate_data.py not found)")

router = APIRouter()

# ==================== PYDANTIC MODELS ====================

class AnalysisResponse(BaseModel):
    """Response model for analysis"""
    # Core risk scores
    risk_score: int = Field(..., ge=0, le=100, description="Overall cognitive risk score")
    risk_category: str = Field(..., description="Risk category (Low/Moderate/High Risk)")
    
    # Cognitive components
    cognitive_risk: int = Field(..., ge=0, le=100, description="Cognitive test component")
    speech_risk: Optional[int] = Field(None, ge=0, le=100, description="Speech analysis component")
    speech_analyzed: bool = Field(..., description="Whether speech was analyzed")
    
    # Model confidence
    confidence_score: Optional[float] = Field(None, description="Model confidence (0-1)")
    
    # Recommendations
    recommendations: List[str] = Field(default=[], description="Personalized recommendations")
    
    # Detailed insights
    insights: Optional[dict] = Field(None, description="Detailed assessment insights")
    
    # Patient tracking
    patient_id: Optional[str] = Field(None, description="Generated patient ID")
    report_saved: bool = Field(False, description="Whether report was saved to Google Docs")
    
    class Config:
        schema_extra = {
            "example": {
                "risk_score": 45,
                "risk_category": "Moderate Risk",
                "cognitive_risk": 45,
                "speech_risk": 30,
                "speech_analyzed": True,
                "confidence_score": 0.85,
                "recommendations": [
                    "Schedule consultation with healthcare provider",
                    "Increase cognitive exercises"
                ],
                "patient_id": "P4F8A2C",
                "report_saved": True
            }
        }

# ==================== MAIN ANALYSIS ENDPOINT ====================

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_assessment(
    # Cognitive test scores (accepting multiple field name formats)
    word_test_score: Optional[float] = Form(None, ge=0, le=100, alias="wordScore"),
    memory_test_score: Optional[float] = Form(None, ge=0, le=100, alias="memoryScore"),
    reaction_time_param: Optional[float] = Form(None, ge=0, alias="reactionTime"),
    
    # Alternative field names
    word_score: Optional[float] = Form(None, ge=0, le=100),
    memory_score: Optional[int] = Form(None, ge=0, le=9),
    reaction_time: Optional[float] = Form(None, ge=0),
    
    # Optional audio file (accepting multiple field names)
    audio_file: Optional[UploadFile] = File(None, alias="audioFile"),
    audio: Optional[UploadFile] = File(None)
):
    """
    Comprehensive dementia risk analysis
    
    **Inputs:**
    - word_test_score/wordScore/word_score: Word unscrambling test (0-100)
    - memory_test_score/memoryScore/memory_score: Memory pattern test (0-100 or 0-9)
    - reaction_time/reactionTime: Reaction time in milliseconds
    - audio_file/audioFile/audio: Optional speech recording (WAV)
    
    **Returns:**
    - Risk score and category
    - Cognitive and speech analysis
    - Personalized recommendations
    - Patient ID
    - Report saved status
    """
    try:
        print("\n" + "="*60)
        print("STARTING DEMENTIA RISK ANALYSIS")
        print("="*60)
        
        # ==================== HANDLE FIELD ALIASES ====================
        # Use the provided values, handling multiple possible field names
        final_word_score = word_test_score or word_score or 0
        final_memory_score = memory_test_score or memory_score or 0
        final_reaction_time = reaction_time_param or reaction_time or 0
        
        # Handle audio file aliases
        final_audio = audio_file or audio
        
        print(f"📊 Cognitive Scores:")
        print(f"   Word Score: {final_word_score}")
        print(f"   Memory Score: {final_memory_score}")
        print(f"   Reaction Time: {final_reaction_time}ms")
        
        # Validate inputs
        if final_word_score == 0 and final_memory_score == 0 and final_reaction_time == 0:
            raise HTTPException(
                status_code=400,
                detail="Missing cognitive test scores. Please provide word_score, memory_score, and reaction_time."
            )
        
        # ==================== STEP 1: COGNITIVE RISK PREDICTION ====================
        print("\n[1/4] Predicting cognitive risk...")
        
        # Convert memory score if needed (0-100 to 0-9 scale)
        memory_for_model = final_memory_score
        if final_memory_score > 9:
            memory_for_model = int(final_memory_score / 100 * 9)
        
        cognitive_risk, cognitive_confidence = predict_cognitive_risk(
            word_score=int(final_word_score),
            memory_score=int(memory_for_model),
            reaction_time=int(final_reaction_time)
        )
        
        print(f"   Cognitive Risk: {cognitive_risk}%")
        print(f"   Model Confidence: {cognitive_confidence:.2f}")
        
        # ==================== STEP 2: SPEECH ANALYSIS ====================
        print("\n[2/4] Analyzing speech (if provided)...")
        speech_risk = None
        speech_confidence = None
        speech_analyzed = False
        
        if final_audio is not None:
            try:
                print(f"   Processing: {final_audio.filename}")
                audio_data = await final_audio.read()
                
                # Validate file size (max 10MB)
                if len(audio_data) > 10 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="Audio file too large (max 10MB)")
                
                # Extract features and predict
                audio_features = extract_audio_features(audio_data)
                feature_array = features_to_array(audio_features)
                speech_risk, speech_confidence = predict_speech_risk(feature_array)
                speech_analyzed = True
                
                print(f"   ✓ Speech Risk: {speech_risk}%")
                print(f"   ✓ Speech Confidence: {speech_confidence:.2f}")
                
            except Exception as e:
                print(f"   ⚠ Speech analysis failed: {e}")
                speech_analyzed = False
        else:
            print("   No audio file provided")
        
        # ==================== STEP 3: CALCULATE FINAL SCORES ====================
        print("\n[3/4] Calculating final risk scores...")
        
        # Calculate overall risk (combining cognitive and speech if available)
        overall_risk = calculate_risk_score(
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk,
            speech_weight=0.3 if speech_analyzed else 0
        )
        
        print(f"   Overall Risk Score: {overall_risk}%")
        
        # Determine risk category
        risk_category = determine_risk_category(overall_risk)
        print(f"   Risk Category: {risk_category}")
        
        # Calculate overall confidence
        if speech_analyzed and speech_confidence:
            overall_confidence = (cognitive_confidence + speech_confidence) / 2
        else:
            overall_confidence = cognitive_confidence
        
        print(f"   Overall Confidence: {overall_confidence:.2f}")
        
        # ==================== STEP 4: GENERATE RECOMMENDATIONS ====================
        print("\n[4/4] Generating recommendations...")
        
        # Generate personalized recommendations
        recommendations = generate_recommendations(
            risk_category=risk_category,
            risk_score=overall_risk,
            cognitive_risk=cognitive_risk,
            speech_analyzed=speech_analyzed
        )
        
        print(f"   Generated {len(recommendations)} recommendations")
        
        # Get detailed insights
        insights = get_risk_insights(
            risk_score=overall_risk,
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk
        )
        
        # ==================== GENERATE PATIENT ID ====================
        # Create unique patient ID for tracking
        patient_id = f"P{uuid.uuid4().hex[:6].upper()}"
        print(f"\n📋 Patient ID: {patient_id}")
        
        # ==================== PREPARE REPORT DATA ====================
        # Build the report data structure
        report_data = {
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Test scores
            "word_score": int(final_word_score),
            "memory_score": int(final_memory_score),
            "reaction_time": int(final_reaction_time),
            
            # Risk analysis
            "cognitive_risk": cognitive_risk,
            "speech_risk": speech_risk if speech_analyzed else None,
            "overall_risk": overall_risk,
            "risk_category": risk_category,
            
            # Confidence scores
            "cognitive_confidence": float(cognitive_confidence),
            "speech_confidence": float(speech_confidence) if speech_confidence else None,
            "overall_confidence": float(overall_confidence),
            
            # Analysis flags
            "speech_analyzed": speech_analyzed,
            
            # Recommendations and insights
            "recommendations": recommendations,
            "insights": insights
        }
        
        # ==================== SAVE TO GOOGLE DOCS ====================
        report_data = {
    "patient_id": patient_id,
    "risk_score": int(overall_risk),
    "risk_category": risk_category,
    "cognitive_risk": int(cognitive_risk),
    "speech_risk": int(speech_risk) if speech_risk is not None else None,
    "speech_analyzed": speech_analyzed,
    "confidence_score": float(overall_confidence),
    "recommendations": recommendations,
    "insights": insights
}

        report_saved = False
        if GDOCS_AVAILABLE:
            print("\n📝 Attempting Google Docs report generation...")
            try:
                # Start Google Docs report generation in background thread
                threading.Thread(
                    target=generate_data,
                    args=(report_data,),
                    daemon=True
                ).start()
                report_saved = True
                print("   ✓ Report generation started (background process)")
            except Exception as e:
                # DO NOT crash the API if Google Docs fails
                report_saved = False
                print(f"   ⚠ Google Docs failed, continuing analysis")
                print(f"   ⚠ Error: {e}")
        
        # ==================== PREPARE RESPONSE ====================
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"Patient ID: {patient_id}")
        print(f"Risk Score: {overall_risk}%")
        print(f"Category: {risk_category}")
        print(f"Confidence: {overall_confidence:.1%}")
        print(f"Speech: {'Analyzed' if speech_analyzed else 'Not provided'}")
        print(f"Report Saved: {'Yes' if report_saved else 'No'}")
        print("="*60 + "\n")
        
        return AnalysisResponse(
            # Core scores
            risk_score=overall_risk,
            risk_category=risk_category,
            
            # Components
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk,
            speech_analyzed=speech_analyzed,
            
            # Confidence
            confidence_score=round(overall_confidence, 2),
            
            # Recommendations
            recommendations=recommendations,
            
            # Detailed info
            insights=insights,
            
            # Patient tracking
            patient_id=patient_id,
            report_saved=report_saved
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# ==================== TEST ENDPOINTS ====================

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "status": "success",
        "message": "Analysis API is operational",
        "version": "1.0.0",
        "features": {
            "cognitive_tests": True,
            "speech_analysis": True,
            "google_docs_reports": GDOCS_AVAILABLE
        },
        "endpoints": {
            "analyze": "/api/analyze - POST - Comprehensive assessment analysis",
            "test": "/api/test - GET - API health check",
            "health": "/api/health - GET - Detailed health status"
        },
        "accepted_field_names": {
            "word_score": ["word_test_score", "wordScore", "word_score"],
            "memory_score": ["memory_test_score", "memoryScore", "memory_score"],
            "reaction_time": ["reaction_time", "reactionTime"],
            "audio": ["audio_file", "audioFile", "audio"]
        }
    }

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    from ai.model import get_model_info
    
    model_info = get_model_info()
    
    return {
        "status": "healthy",
        "service": "dementia-analysis-api",
        "version": "1.0.0",
        "features": {
            "ml_models": model_info,
            "google_docs_integration": GDOCS_AVAILABLE
        }
    }

@router.get("/reports/status")
async def reports_status():
    """Check if Google Docs report generation is available"""
    return {
        "google_docs_available": GDOCS_AVAILABLE,
        "message": "Google Docs report generation is enabled" if GDOCS_AVAILABLE else "Google Docs report generation is not configured",
        "setup_instructions": [
            "1. Install: pip install google-auth google-api-python-client",
            "2. Create service_account.json file",
            "3. Set DOCUMENT_ID in generate_data.py",
            "4. Share Google Doc with service account email"
        ] if not GDOCS_AVAILABLE else []
    }