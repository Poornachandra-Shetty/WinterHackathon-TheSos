"""
Machine Learning Model Module
Handles model loading and predictions for dementia risk assessment
"""
import numpy as np
import joblib
import os
from typing import Tuple, Optional

# Global variables for models
cognitive_model = None
speech_model = None
cognitive_scaler = None
speech_scaler = None
models_loaded = False

def load_model():
    """
    Load pre-trained ML models from disk
    Falls back to rule-based system if models not available
    """
    global cognitive_model, speech_model, cognitive_scaler, speech_scaler, models_loaded
    
    # Get models directory path
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    try:
        # Load cognitive assessment model
        cognitive_model_path = os.path.join(model_dir, 'ai_model.pkl')
        if os.path.exists(cognitive_model_path):
            cognitive_model = joblib.load(cognitive_model_path)
            print("✓ Cognitive model loaded successfully")
        else:
            print("⚠ Cognitive model not found at:", cognitive_model_path)
        
        # Load feature scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        if os.path.exists(scaler_path):
            cognitive_scaler = joblib.load(scaler_path)
            print("✓ Feature scaler loaded successfully")
        else:
            print("⚠ Scaler not found")
        
        # Check if models loaded successfully
        if cognitive_model is not None:
            models_loaded = True
            print("✓ ML models ready for predictions")
        else:
            print("⚠ Using rule-based fallback system")
            models_loaded = False
        
    except Exception as e:
        print(f"⚠ Warning: Could not load ML models - {e}")
        print("⚠ Using rule-based fallback system")
        models_loaded = False

def predict_cognitive_risk(
    word_score: int,
    memory_score: int,
    reaction_time: int
) -> Tuple[int, float]:
    """
    Predict cognitive risk using ML model or fallback
    
    Args:
        word_score: Score from word unscrambling test (0-100)
        memory_score: Score from memory pattern test (0-9)
        reaction_time: Reaction time in milliseconds
    
    Returns:
        Tuple of (risk_score: 0-100, confidence: 0-1)
    """
    if models_loaded and cognitive_model is not None:
        try:
            # Prepare features for ML model
            features = np.array([[
                word_score,
                memory_score,
                reaction_time,
                reaction_time / 1000,  # reaction time in seconds
                memory_score / 9.0,    # normalized memory score (0-1)
                word_score / 100.0,    # normalized word score (0-1)
                1 if reaction_time < 300 else (2 if reaction_time < 500 else 3)  # reaction category
            ]])
            
            # Scale features if scaler available
            if cognitive_scaler is not None:
                features = cognitive_scaler.transform(features)
            
            # Make prediction
            if hasattr(cognitive_model, 'predict_proba'):
                # Classification model with probability output
                proba = cognitive_model.predict_proba(features)[0]
                # proba = [prob_low, prob_moderate, prob_high]
                risk_score = int(proba[1] * 50 + proba[2] * 100)
                confidence = float(np.max(proba))
            else:
                # Regression model or classifier without proba
                prediction = cognitive_model.predict(features)[0]
                risk_score = int(prediction * 100)
                confidence = 0.85
            
            return max(0, min(100, risk_score)), confidence
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            return predict_cognitive_risk_fallback(word_score, memory_score, reaction_time)
    else:
        return predict_cognitive_risk_fallback(word_score, memory_score, reaction_time)

def predict_speech_risk(audio_features: np.ndarray) -> Tuple[int, float]:
    """
    Predict speech-based dementia risk using ML model
    
    Args:
        audio_features: Numpy array of extracted audio features
    
    Returns:
        Tuple of (risk_score: 0-100, confidence: 0-1)
    """
    if models_loaded and speech_model is not None:
        try:
            # Scale features if scaler available
            if speech_scaler is not None:
                audio_features = speech_scaler.transform(audio_features)
            
            # Make prediction
            if hasattr(speech_model, 'predict_proba'):
                proba = speech_model.predict_proba(audio_features)[0]
                risk_score = int(proba[1] * 50 + proba[2] * 100)
                confidence = float(np.max(proba))
            else:
                prediction = speech_model.predict(audio_features)[0]
                risk_score = int(prediction * 100)
                confidence = 0.80
            
            return max(0, min(100, risk_score)), confidence
            
        except Exception as e:
            print(f"Speech ML prediction error: {e}")
            return predict_speech_risk_fallback()
    else:
        return predict_speech_risk_fallback()

def predict_cognitive_risk_fallback(
    word_score: int,
    memory_score: int,
    reaction_time: int
) -> Tuple[int, float]:
    """
    Rule-based fallback prediction when ML models unavailable
    Uses weighted scoring based on clinical thresholds
    
    Args:
        word_score: Score from word test (0-100)
        memory_score: Score from memory test (0-9)
        reaction_time: Reaction time in milliseconds
    
    Returns:
        Tuple of (risk_score, confidence)
    """
    # Calculate individual risk components
    word_risk = 100 - word_score
    
    # Memory score risk (0-9 scale normalized to 0-100)
    memory_risk = 100 - (memory_score * 11.11)
    
    # Reaction time risk based on clinical thresholds
    if reaction_time < 300:
        reaction_risk = 10  # Excellent
    elif reaction_time < 500:
        reaction_risk = 30  # Good
    elif reaction_time < 700:
        reaction_risk = 50  # Average
    elif reaction_time < 900:
        reaction_risk = 70  # Below average
    else:
        reaction_risk = 90  # Concerning
    
    # Weighted average (memory is most important for dementia)
    overall_risk = int(
        (word_risk * 0.25) +      # 25% weight on word unscrambling
        (memory_risk * 0.50) +     # 50% weight on memory
        (reaction_risk * 0.25)     # 25% weight on reaction time
    )
    # Confidence based on consistency of inputs
    word_norm = word_score / 100
    memory_norm = memory_score / 9
    reaction_norm = min(reaction_time / 1500, 1)

    variance = (
    abs(word_norm - memory_norm) +
    abs(memory_norm - reaction_norm)
)

    confidence = round(max(0.45, min(0.85, 1 - variance / 2)), 2)
    
    return max(0, min(100, overall_risk)), confidence

def predict_speech_risk_fallback() -> Tuple[int, float]:
    """
    Fallback for speech analysis when ML model unavailable
    Returns moderate risk with low confidence
    
    Returns:
        Tuple of (risk_score, confidence)
    """
    import random
    # Random risk in moderate range
    risk = random.randint(30, 60)
    confidence = 0.50  # Low confidence for fallback
    return risk, confidence

def get_model_info() -> dict:
    """
    Get information about loaded models
    
    Returns:
        Dictionary with model information
    """
    return {
        "models_loaded": models_loaded,
        "cognitive_model": cognitive_model is not None,
        "speech_model": speech_model is not None,
        "scaler_available": cognitive_scaler is not None,
        "prediction_mode": "ML-based" if models_loaded else "Rule-based"
    }
