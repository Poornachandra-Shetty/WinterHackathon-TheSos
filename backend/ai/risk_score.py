"""
Risk Score Calculation and Assessment Module
Handles risk scoring, categorization, and recommendations
"""
from typing import List, Dict, Optional

def calculate_risk_score(
    cognitive_risk: int,
    speech_risk: Optional[int] = None,
    speech_weight: float = 0.3
) -> int:
    """
    Calculate overall risk score from multiple assessments
    
    Args:
        cognitive_risk: Risk from cognitive tests (0-100)
        speech_risk: Risk from speech analysis (0-100), optional
        speech_weight: Weight for speech component (default 0.3 = 30%)
    
    Returns:
        Overall risk score (0-100)
    """
    if speech_risk is not None:
        cognitive_weight = 1.0 - speech_weight
        overall_risk = int(
            (cognitive_risk * cognitive_weight) + (speech_risk * speech_weight)
        )
    else:
        overall_risk = cognitive_risk
    
    return max(0, min(100, overall_risk))

def determine_risk_category(risk_score: int) -> str:
    """
    Determine risk category based on risk score
    
    Categories based on clinical thresholds:
    - Low Risk: 0-29 (minimal concern)
    - Moderate Risk: 30-59 (monitoring recommended)
    - High Risk: 60-100 (evaluation recommended)
    
    Args:
        risk_score: Overall risk score (0-100)
    
    Returns:
        Risk category: "Low Risk", "Moderate Risk", or "High Risk"
    """
    if risk_score < 30:
        return "Low Risk"
    elif risk_score < 60:
        return "Moderate Risk"
    else:
        return "High Risk"

def generate_recommendations(
    risk_category: str,
    risk_score: int,
    cognitive_risk: int,
    speech_analyzed: bool
) -> List[str]:
    """
    Generate personalized recommendations based on assessment results
    
    Args:
        risk_category: Risk category (Low/Moderate/High)
        risk_score: Overall risk score (0-100)
        cognitive_risk: Cognitive component risk score
        speech_analyzed: Whether speech was analyzed
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    if risk_category == "Low Risk":
        recommendations = [
            "Continue maintaining a healthy lifestyle with regular physical exercise",
            "Engage in mentally stimulating activities such as puzzles, reading, and learning new skills",
            "Maintain strong social connections and stay engaged with your community",
            "Consider annual cognitive health check-ups as a preventive measure",
            "Keep a balanced diet rich in omega-3 fatty acids, antioxidants, and whole foods",
            "Ensure adequate sleep (7-9 hours) and manage stress through relaxation techniques"
        ]
    
    elif risk_category == "Moderate Risk":
        recommendations = [
            "Schedule a consultation with your healthcare provider for a comprehensive cognitive evaluation",
            "Increase frequency of cognitive exercises and brain training activities",
            "Monitor changes in memory, attention, or cognitive function over the next 3-6 months",
            "Consider lifestyle modifications including improved diet, regular exercise, and quality sleep",
            "Discuss these results with family members or caregivers for support",
            "Reduce stress and practice mindfulness, meditation, or other relaxation techniques",
            "Limit alcohol consumption and avoid smoking"
        ]
        
        # Add specific recommendations based on cognitive scores
        if cognitive_risk > 50:
            recommendations.insert(2, "Focus on memory exercises and cognitive rehabilitation programs")
        
        # Add speech-specific recommendations
        if speech_analyzed:
            recommendations.append("Consider speech therapy consultation if communication difficulties are noticed")
    
    else:  # High Risk
        recommendations = [
            "Seek immediate consultation with a neurologist or cognitive health specialist",
            "Schedule a comprehensive neuropsychological assessment and medical evaluation",
            "Discuss diagnostic testing options (MRI, cognitive assessments) with your healthcare provider",
            "Explore treatment options, medications, and therapeutic interventions",
            "Consider joining support groups for patients and caregivers",
            "Implement safety measures at home and create an advance care plan with family",
            "Explore clinical trials and research opportunities if appropriate",
            "Arrange regular follow-up appointments to monitor cognitive changes"
        ]
        
        # Add speech-specific recommendations for high risk
        if speech_analyzed:
            recommendations.insert(3, "Speech pathology evaluation strongly recommended for communication support")
    
    return recommendations

def get_risk_insights(
    risk_score: int,
    cognitive_risk: int,
    speech_risk: Optional[int] = None
) -> Dict[str, any]:
    """
    Generate detailed insights about the risk assessment
    Provides explanations and analysis of results
    
    Args:
        risk_score: Overall risk score (0-100)
        cognitive_risk: Cognitive component risk
        speech_risk: Speech component risk (optional)
    
    Returns:
        Dictionary with risk insights and explanations
    """
    insights = {
        "overall_assessment": "",
        "cognitive_assessment": "",
        "speech_assessment": "",
        "key_concerns": [],
        "positive_indicators": [],
        "severity_level": ""
    }
    
    # Overall assessment explanation
    if risk_score < 30:
        insights["overall_assessment"] = ("Your assessment indicates low risk for cognitive impairment. "
                                         "Cognitive function appears to be within normal range for your demographic.")
        insights["severity_level"] = "Minimal"
    elif risk_score < 60:
        insights["overall_assessment"] = ("Your assessment indicates moderate risk for cognitive changes. "
                                         "Some cognitive variations detected that warrant monitoring and follow-up.")
        insights["severity_level"] = "Moderate"
    else:
        insights["overall_assessment"] = ("Your assessment indicates elevated risk for cognitive impairment. "
                                         "Professional medical evaluation is strongly recommended.")
        insights["severity_level"] = "Elevated"
    
    # Cognitive assessment details
    if cognitive_risk < 30:
        insights["cognitive_assessment"] = ("Cognitive test performance is strong across memory, processing speed, "
                                           "and pattern recognition tasks.")
        insights["positive_indicators"].append("Strong cognitive test performance")
        insights["positive_indicators"].append("Good memory retention")
        insights["positive_indicators"].append("Normal reaction time")
    elif cognitive_risk < 60:
        insights["cognitive_assessment"] = ("Cognitive test results show some areas that may benefit from "
                                           "attention and continued monitoring over time.")
        insights["key_concerns"].append("Moderate cognitive test scores requiring monitoring")
        
        if cognitive_risk > 45:
            insights["key_concerns"].append("Memory performance below optimal range")
    else:
        insights["cognitive_assessment"] = ("Cognitive test results indicate areas of concern that should be "
                                           "evaluated by a qualified healthcare professional.")
        insights["key_concerns"].append("Cognitive test scores indicating need for professional evaluation")
        insights["key_concerns"].append("Memory and processing speed concerns")
    
    # Speech assessment details (if available)
    if speech_risk is not None:
        if speech_risk < 30:
            insights["speech_assessment"] = ("Speech patterns show normal characteristics with clear articulation, "
                                            "appropriate pace, and typical acoustic features.")
            insights["positive_indicators"].append("Normal speech patterns and fluency")
        elif speech_risk < 60:
            insights["speech_assessment"] = ("Speech analysis detected some patterns that may warrant "
                                            "further monitoring or evaluation.")
            insights["key_concerns"].append("Speech pattern variations noted")
        else:
            insights["speech_assessment"] = ("Speech analysis indicates patterns that should be evaluated "
                                            "by a speech-language pathologist or healthcare professional.")
            insights["key_concerns"].append("Speech patterns requiring professional assessment")
            insights["key_concerns"].append("Possible communication difficulties")
    else:
        insights["speech_assessment"] = "Speech analysis was not performed in this assessment."
    
    # Add guidance based on results
    insights["next_steps"] = get_next_steps(risk_score)
    
    return insights

def get_next_steps(risk_score: int) -> List[str]:
    """
    Get recommended next steps based on risk score
    
    Args:
        risk_score: Overall risk score (0-100)
    
    Returns:
        List of next steps
    """
    if risk_score < 30:
        return [
            "Continue current healthy lifestyle practices",
            "Repeat screening annually for ongoing monitoring",
            "Stay informed about cognitive health"
        ]
    elif risk_score < 60:
        return [
            "Schedule appointment with primary care physician",
            "Repeat assessment in 3-6 months",
            "Implement lifestyle modifications",
            "Track cognitive changes over time"
        ]
    else:
        return [
            "Schedule immediate consultation with neurologist",
            "Undergo comprehensive medical evaluation",
            "Discuss diagnostic testing options",
            "Develop care plan with healthcare team",
            "Inform family members and caregivers"
        ]

def format_risk_report(
    risk_score: int,
    risk_category: str,
    cognitive_risk: int,
    speech_risk: Optional[int],
    recommendations: List[str],
    insights: Dict
) -> str:
    """
    Format a complete risk assessment report as text
    
    Returns:
        Formatted report string
    """
    report = f"""
    ========================================
    DEMENTIA RISK ASSESSMENT REPORT
    ========================================
    
    Overall Risk Score: {risk_score}/100
    Risk Category: {risk_category}
    Severity Level: {insights.get('severity_level', 'N/A')}
    
    COMPONENT SCORES:
    - Cognitive Assessment: {cognitive_risk}/100
    - Speech Analysis: {speech_risk if speech_risk else 'Not performed'}/100
    
    ASSESSMENT SUMMARY:
    {insights.get('overall_assessment', '')}
    
    COGNITIVE EVALUATION:
    {insights.get('cognitive_assessment', '')}
    
    SPEECH EVALUATION:
    {insights.get('speech_assessment', '')}
    
    KEY CONCERNS:
    """
    
    for concern in insights.get('key_concerns', []):
        report += f"  - {concern}\n"
    
    report += "\n    POSITIVE INDICATORS:\n"
    for indicator in insights.get('positive_indicators', []):
        report += f"  - {indicator}\n"
    
    report += "\n    RECOMMENDATIONS:\n"
    for i, rec in enumerate(recommendations, 1):
        report += f"  {i}. {rec}\n"
    
    report += "\n    NEXT STEPS:\n"
    for step in insights.get('next_steps', []):
        report += f"  - {step}\n"
    
    report += """
    ========================================
    DISCLAIMER: This is a screening tool only and does not constitute 
    a medical diagnosis. Consult with a qualified healthcare professional 
    for proper evaluation and diagnosis.
    ========================================
    """
    
    return report