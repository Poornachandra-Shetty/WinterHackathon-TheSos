from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from typing import Optional
import sys
import os

# Add parent directory to path to import from ai/ folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.model import predict_dementia_risk, predict_cognitive_only
from ai.audio_features import extract_speech_features
from ai.risk_score import calculate_final_risk

# Create API router
router = APIRouter()


@router.post("/analyze")
async def analyze_cognitive_assessment(
    word_score: float = Form(...),
    memory_score: float = Form(...),
    reaction_time: float = Form(...),
    audio_file: Optional[UploadFile] = File(None)
):
    """
    Analyze cognitive assessment data and return dementia risk prediction.
    
    Args:
        word_score: Score from jumbled word task (0-100)
        memory_score: Maximum pattern length remembered in box-glow task
        reaction_time: Reaction time in milliseconds
        audio_file: Optional WAV audio file for speech analysis
    
    Returns:
        JSON response with risk score and category
    """
    
    try:
        # Validate input ranges
        if not (0 <= word_score <= 100):
            raise HTTPException(status_code=400, detail="word_score must be between 0 and 100")
        if memory_score < 0:
            raise HTTPException(status_code=400, detail="memory_score must be non-negative")
        if reaction_time < 0:
            raise HTTPException(status_code=400, detail="reaction_time must be non-negative")
        
        # Check if audio file is provided
        if audio_file is not None:
            # Read audio file content
            audio_content = await audio_file.read()
            
            # Extract numeric speech features from the audio
            speech_features = extract_speech_features(audio_content)
            
            # Predict dementia risk using cognitive + speech features
            cognitive_risk = predict_dementia_risk(
                word_score=word_score,
                memory_score=memory_score,
                reaction_time=reaction_time,
                speech_features=speech_features
            )
            
            # For this implementation, we use the combined prediction as both scores
            speech_risk = cognitive_risk  # Can be separated if using different models
            
        else:
            # No audio provided - use cognitive features only
            cognitive_risk = predict_cognitive_only(
                word_score=word_score,
                memory_score=memory_score,
                reaction_time=reaction_time
            )
            
            # Set speech risk to None or default value
            speech_risk = cognitive_risk  # Use same value for consistent scoring
        
        # Calculate final risk score and category
        final_result = calculate_final_risk(
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk
        )
        
        # Return JSON response with prediction results
        return {
            "success": True,
            "risk_score": final_result['percentage'],
            "risk_category": final_result['category'],
            "cognitive_risk": round(cognitive_risk * 100, 2),
            "speech_analyzed": audio_file is not None
        }
    
    except ValueError as e:
        # Handle validation or model errors
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {
        "status": "healthy",
        "message": "Analysis endpoint is ready"
    }