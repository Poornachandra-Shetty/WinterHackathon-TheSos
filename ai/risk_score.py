def calculate_final_risk(cognitive_risk, speech_risk, behavioral_risk=None):
    """
    Calculate final dementia risk score by combining multiple AI model outputs.
    
    Args:
        cognitive_risk (float): Probability score from cognitive tests (0.0 to 1.0)
        speech_risk (float): Probability score from speech analysis (0.0 to 1.0)
        behavioral_risk (float, optional): Probability score from behavioral analysis (0.0 to 1.0)
    
    Returns:
        dict: Contains 'percentage' (0-100) and 'category' (Low/Moderate/High)
    """
    
    # Define weights for each risk component
    if behavioral_risk is not None:
        # If behavioral risk is provided, distribute weights across all three
        cognitive_weight = 0.5
        speech_weight = 0.3
        behavioral_weight = 0.2
        
        # Calculate weighted average of all three risk scores
        final_risk = (
            cognitive_risk * cognitive_weight +
            speech_risk * speech_weight +
            behavioral_risk * behavioral_weight
        )
    else:
        # Default: only cognitive and speech risks
        cognitive_weight = 0.6
        speech_weight = 0.4
        
        # Calculate weighted average of cognitive and speech risks
        final_risk = (
            cognitive_risk * cognitive_weight +
            speech_risk * speech_weight
        )
    
    # Convert from probability (0-1) to percentage (0-100)
    risk_percentage = final_risk * 100
    
    # Determine risk category based on final score
    risk_category = get_risk_category(final_risk)
    
    return {
        'percentage': round(risk_percentage, 2),
        'category': risk_category
    }


def get_risk_category(risk_score):
    """
    Categorize numeric risk score into Low/Moderate/High risk levels.
    
    Args:
        risk_score (float): Probability between 0.0 and 1.0
    
    Returns:
        str: Risk category
    """
    # Thresholds for risk categorization
    # Low Risk: < 30% probability
    # Moderate Risk: 30% - 60% probability
    # High Risk: > 60% probability
    
    if risk_score < 0.3:
        return "Low Risk"
    elif risk_score < 0.6:
        return "Moderate Risk"
    else:
        return "High Risk"


def get_risk_interpretation(risk_percentage):
    """
    Provide a human-readable interpretation of the risk score.
    
    Args:
        risk_percentage (float): Risk percentage (0-100)
    
    Returns:
        str: Interpretation message
    """
    if risk_percentage < 30:
        return "Your cognitive assessment shows healthy performance. Continue maintaining an active lifestyle."
    elif risk_percentage < 60:
        return "Some cognitive indicators suggest monitoring may be beneficial. Consider consulting a healthcare professional."
    else:
        return "Your assessment suggests elevated risk factors. We recommend seeking professional medical evaluation."


def validate_risk_inputs(cognitive_risk, speech_risk, behavioral_risk=None):
    """
    Validate that input risk scores are within valid range (0.0 to 1.0).
    
    Args:
        cognitive_risk (float): Cognitive risk score
        speech_risk (float): Speech risk score
        behavioral_risk (float, optional): Behavioral risk score
    
    Returns:
        bool: True if all inputs are valid
    
    Raises:
        ValueError: If any input is outside the valid range
    """
    # Check cognitive risk
    if not 0.0 <= cognitive_risk <= 1.0:
        raise ValueError(f"Cognitive risk must be between 0.0 and 1.0, got {cognitive_risk}")
    
    # Check speech risk
    if not 0.0 <= speech_risk <= 1.0:
        raise ValueError(f"Speech risk must be between 0.0 and 1.0, got {speech_risk}")
    
    # Check behavioral risk if provided
    if behavioral_risk is not None:
        if not 0.0 <= behavioral_risk <= 1.0:
            raise ValueError(f"Behavioral risk must be between 0.0 and 1.0, got {behavioral_risk}")
    
    return True