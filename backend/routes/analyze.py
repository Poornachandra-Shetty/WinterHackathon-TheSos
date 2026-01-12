"""
Analysis API Routes
Handles all cognitive and speech analysis endpoints
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.model import predict_cognitive_risk, predict_speech_risk
from ai.audio_features import extract_audio_features, features_to_array
from ai.risk_score import (
    calculate_risk_score,
    determine_risk_category,
    generate_recommendations,
    get_risk_insights
)

# Create router
router = APIRouter()

# ==================== PYDANTIC MODELS ====================

class AnalysisResponse(BaseModel):
    """Response model for analysis endpoints"""
    risk_score: int = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    risk_category: str = Field(..., description="Risk category: Low/Moderate/High Risk")
    cognitive_risk: int = Field(..., ge=0, le=100, description="Cognitive component risk score")
    speech_risk: Optional[int] = Field(None, ge=0, le=100, description="Speech component risk score")
    speech_analyzed: bool = Field(..., description="Whether speech analysis was performed")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Model confidence (0-1)")
    recommendations: List[str] = Field(default=[], description="Personalized recommendations")
    insights: Optional[dict] = Field(None, description="Detailed assessment insights")

    class Config:
        schema_extra = {
            "example": {
                "risk_score": 35,
                "risk_category": "Moderate Risk",
                "cognitive_risk": 40,
                "speech_risk": 25,
                "speech_analyzed": True,
                "confidence_score": 0.85,
                "recommendations": [
                    "Schedule consultation with healthcare provider",
                    "Increase cognitive exercises"
                ],
                "insights": {
                    "overall_assessment": "Moderate risk detected...",
                    "key_concerns": ["Memory performance below optimal"],
                    "positive_indicators": ["Normal reaction time"]
                }
            }
        }

# ==================== API ENDPOINTS ====================

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_assessment(
    word_score: int = Form(..., ge=0, le=100, description="Word unscrambling test score (0-100)"),
    memory_score: int = Form(..., ge=0, le=9, description="Memory pattern test score (0-9)"),
    reaction_time: int = Form(..., ge=0, description="Reaction time in milliseconds"),
    audio_file: UploadFile = File(None, description="Optional WAV audio file for speech analysis")
):
    """
    Comprehensive dementia risk analysis endpoint
    
    Analyzes cognitive test results and optional speech audio to calculate
    overall dementia risk score with personalized recommendations.
    
    **Inputs:**
    - word_score: Score from word unscrambling test (0-100)
    - memory_score: Number of correct memory sequences (0-9)
    - reaction_time: Average reaction time in milliseconds
    - audio_file: Optional speech recording (WAV format)
    
    **Returns:**
    - Comprehensive risk assessment with scores, category, and recommendations
    """
    try:
        # Validate inputs
        if word_score < 0 or word_score > 100:
            raise HTTPException(status_code=400, detail="word_score must be between 0 and 100")
        if memory_score < 0 or memory_score > 9:
            raise HTTPException(status_code=400, detail="memory_score must be between 0 and 9")
        if reaction_time < 0:
            raise HTTPException(status_code=400, detail="reaction_time must be positive")
        
        # Step 1: Predict cognitive risk
        cognitive_risk, cognitive_confidence = predict_cognitive_risk(
            word_score=word_score,
            memory_score=memory_score,
            reaction_time=reaction_time
        )
        
        print(f"Cognitive Risk: {cognitive_risk}%, Confidence: {cognitive_confidence}")
        
        # Step 2: Analyze speech if audio provided
        speech_risk = None
        speech_confidence = None
        speech_analyzed = False
        
        if audio_file is not None:
            try:
                print(f"Processing audio file: {audio_file.filename}")
                
                # Read audio data
                audio_data = await audio_file.read()
                
                # Validate file size (max 10MB)
                if len(audio_data) > 10 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="Audio file too large (max 10MB)")
                
                # Extract audio features
                audio_features = extract_audio_features(audio_data)
                feature_array = features_to_array(audio_features)
                
                # Predict speech risk
                speech_risk, speech_confidence = predict_speech_risk(feature_array)
                speech_analyzed = True
                
                print(f"Speech Risk: {speech_risk}%, Confidence: {speech_confidence}")
                
            except Exception as e:
                print(f"Speech analysis error: {e}")
                # Continue without speech analysis
                speech_analyzed = False
        
        # Step 3: Calculate overall risk score
        overall_risk = calculate_risk_score(
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk,
            speech_weight=0.3 if speech_analyzed else 0
        )
        
        # Step 4: Determine risk category
        risk_category = determine_risk_category(overall_risk)
        
        # Step 5: Calculate overall confidence
        if speech_analyzed and speech_confidence:
            confidence = round((cognitive_confidence + speech_confidence) / 2, 2)
        else:
            confidence = round(cognitive_confidence, 2)
        
        # Step 6: Generate personalized recommendations
        recommendations = generate_recommendations(
            risk_category=risk_category,
            risk_score=overall_risk,
            cognitive_risk=cognitive_risk,
            speech_analyzed=speech_analyzed
        )
        
        # Step 7: Get detailed insights
        insights = get_risk_insights(
            risk_score=overall_risk,
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk
        )
        
        print(f"Analysis Complete - Overall Risk: {overall_risk}%, Category: {risk_category}")
        
        # Return comprehensive response
        return AnalysisResponse(
            risk_score=overall_risk,
            risk_category=risk_category,
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk,
            speech_analyzed=speech_analyzed,
            confidence_score=confidence,
            recommendations=recommendations,
            insights=insights
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/test")
async def test_endpoint():
    """
    Test endpoint to verify API is working
    
    Returns basic API status and available endpoints
    """
    return {
        "status": "success",
        "message": "Analysis API is operational",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze - POST - Comprehensive assessment analysis",
            "test": "/api/test - GET - API health check"
        },
        "supported_formats": {
            "audio": ["WAV"],
            "cognitive_tests": ["word_score", "memory_score", "reaction_time"]
        }
    }

@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    from ai.model import get_model_info
    
    model_info = get_model_info()
    
    return {
        "status": "healthy",
        "service": "analysis-api",
        "models": model_info
    }