import joblib
import pandas as pd
import numpy as np
import os

# Load the pre-trained machine learning model
MODEL_PATH = 'ai_model.pkl'

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"Warning: Model file '{MODEL_PATH}' not found. Ensure the model is trained and saved.")
    model = None


def predict_dementia_risk(word_score, memory_score, reaction_time, speech_features):
    """
    Predict dementia risk based on cognitive tests and speech analysis.
    
    Args:
        word_score (float): Score from jumbled word task (0-100)
        memory_score (float): Maximum pattern length remembered in box-glow task
        reaction_time (float): Reaction time in milliseconds
        speech_features (list or np.array): Numeric feature vector from speech audio
    
    Returns:
        float: Probability of dementia risk (0.0 to 1.0)
    """
    if model is None:
        raise ValueError("Model not loaded. Cannot make predictions.")
    
    # Create DataFrame for cognitive features with proper column names
    cognitive_data = pd.DataFrame({
        'word_score': [word_score],
        'memory_score': [memory_score],
        'reaction_time': [reaction_time]
    })
    
    # Convert speech features to numpy array if needed
    if isinstance(speech_features, list):
        speech_features = np.array(speech_features)
    
    # Reshape speech features to 2D array (1 sample, n features)
    speech_array = speech_features.reshape(1, -1)
    
    # Combine cognitive features and speech features
    # Concatenate along columns (axis=1)
    combined_features = np.concatenate([cognitive_data.values, speech_array], axis=1)
    
    # Perform inference using the trained model
    probabilities = model.predict_proba(combined_features)
    
    # Return the probability of dementia (second column: positive class)
    risk_score = probabilities[0][1]
    
    return risk_score


def predict_cognitive_only(word_score, memory_score, reaction_time):
    """
    Predict dementia risk using only cognitive test features (no speech).
    
    Args:
        word_score (float): Score from jumbled word task (0-100)
        memory_score (float): Maximum pattern length remembered
        reaction_time (float): Reaction time in milliseconds
    
    Returns:
        float: Probability of dementia risk (0.0 to 1.0)
    """
    if model is None:
        raise ValueError("Model not loaded. Cannot make predictions.")
    
    # Create DataFrame with cognitive features
    input_data = pd.DataFrame({
        'word_score': [word_score],
        'memory_score': [memory_score],
        'reaction_time': [reaction_time]
    })
    
    # Get probability predictions
    probabilities = model.predict_proba(input_data)
    
    # Return dementia risk probability
    risk_score = probabilities[0][1]
    
    return risk_score


def get_risk_category(risk_score):
    """
    Convert numeric risk score to categorical risk level.
    
    Args:
        risk_score (float): Probability between 0.0 and 1.0
    
    Returns:
        str: Risk category (Low/Moderate/High)
    """
    if risk_score < 0.3:
        return "Low Risk"
    elif risk_score < 0.6:
        return "Moderate Risk"
    else:
        return "High Risk"