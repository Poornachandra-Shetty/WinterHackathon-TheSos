"""
generate_data.py - Comprehensive Google Docs Report Generator
Generates detailed dementia screening reports with all calculation details

Requirements:
    pip install google-auth google-auth-oauthlib google-api-python-client

Setup:
    1. Create a Google Cloud Project
    2. Enable Google Docs API
    3. Create a Service Account and download JSON key as 'service_account.json'
    4. Share your Google Doc with the service account email (found in JSON file)
"""

import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ==================== CONFIGURATION ====================

# Google Docs Document ID (get from URL: docs.google.com/document/d/{DOCUMENT_ID}/edit)
DOCUMENT_ID = "16-n9SbCHwJQinQlolEDDSah7aMzbPBsZskJDNdhS_xw"  # Replace with your actual document ID

# Service account JSON file (must be in same directory)
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Google Docs API scopes
SCOPES = ['https://www.googleapis.com/auth/documents']

# Enable/disable Google Docs integration
ENABLE_GOOGLE_DOCS = True


# ==================== AUTHENTICATION ====================

def authenticate_google_docs():
    """
    Authenticate using service account credentials
    
    Returns:
        Google Docs API service object
    """
    try:
        # Load service account credentials from JSON file
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        
        # Build the Google Docs API service
        service = build('docs', 'v1', credentials=credentials)
        
        print("✓ Successfully authenticated with Google Docs API")
        return service
        
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        raise


# ==================== COMPREHENSIVE REPORT GENERATION ====================

def generate_data(result):
    """
    Generate a comprehensive dementia screening report and append to Google Docs
    
    Args:
        result (dict): Dictionary containing analysis results with fields:
            - patient_id (str): Unique patient identifier
            - risk_score (int): Overall risk score (0-100)
            - risk_category (str): Risk category (Low/Moderate/High Risk)
            - cognitive_risk (int): Cognitive component risk
            - speech_risk (int, optional): Speech analysis risk
            - speech_analyzed (bool): Whether speech was analyzed
            - confidence_score (float): Model confidence (0-1)
            - recommendations (list): List of recommendations
            - insights (dict, optional): Detailed insights
            
    Example:
        result = {
            "patient_id": "P12345",
            "risk_score": 45,
            "risk_category": "Moderate Risk",
            "cognitive_risk": 48,
            "speech_risk": 38,
            "speech_analyzed": True,
            "confidence_score": 0.85,
            "recommendations": ["Schedule consultation", "Increase cognitive exercises"],
            "insights": {...}
        }
    """
    
    # Check if Google Docs is enabled
    if not ENABLE_GOOGLE_DOCS:
        print("⚠ Google Docs disabled — skipping report generation")
        return
    
    # Validate that result is not None
    if result is None:
        print("✗ Error: No result data provided")
        return
    
    try:
        # Step 1: Authenticate with Google Docs API
        service = authenticate_google_docs()
        
        # Step 2: Extract data from result dictionary
        patient_id = result.get('patient_id', 'Unknown')
        risk_score = result.get('risk_score', 0)
        risk_category = result.get('risk_category', 'Unknown')
        cognitive_risk = result.get('cognitive_risk', 0)
        speech_risk = result.get('speech_risk', None)
        speech_analyzed = result.get('speech_analyzed', False)
        confidence_score = result.get('confidence_score', 0)
        recommendations = result.get('recommendations', [])
        insights = result.get('insights', {})
        
        # Step 3: Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Step 4: Build comprehensive report content
        report_content = generate_comprehensive_report(
            patient_id=patient_id,
            timestamp=timestamp,
            risk_score=risk_score,
            risk_category=risk_category,
            cognitive_risk=cognitive_risk,
            speech_risk=speech_risk,
            speech_analyzed=speech_analyzed,
            confidence_score=confidence_score,
            recommendations=recommendations,
            insights=insights
        )
        
        # Step 5: Append report to Google Docs
        append_to_google_docs(service, report_content)
        print(f"✓ Comprehensive report generated for Patient {patient_id}")
        print(f"  Risk Score: {risk_score}%")
        print(f"  Category: {risk_category}")
        print(f"  Confidence: {confidence_score * 100:.1f}%")
        
    except Exception as e:
        print(f"✗ Failed to generate report: {e}")
        # Don't raise - allow API to continue even if Google Docs fails
        import traceback
        traceback.print_exc()


# ==================== REPORT FORMATTING ====================

def generate_comprehensive_report(
    patient_id, timestamp, risk_score, risk_category, 
    cognitive_risk, speech_risk, speech_analyzed, 
    confidence_score, recommendations, insights
):
    """
    Generate comprehensive report with all calculation details
    """
    
    # Convert confidence to percentage
    confidence_percentage = confidence_score * 100 if isinstance(confidence_score, float) else confidence_score
    
    # Get risk indicator emoji
    risk_emoji = get_risk_emoji(risk_category)
    
    # Get confidence level description
    confidence_level = get_confidence_level(confidence_percentage)
    
    # Build the detailed report
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      DEMENTIA SCREENING REPORT                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT METADATA                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
  Generated:        {timestamp}
  Patient ID:       {patient_id}
  Report Type:      Comprehensive Cognitive & Speech Analysis

┌─────────────────────────────────────────────────────────────────────────────┐
│ OVERALL ASSESSMENT                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
  {risk_emoji} RISK CATEGORY:     {risk_category}
  ⚡ RISK SCORE:        {risk_score}% (out of 100)
  🎯 CONFIDENCE:        {confidence_percentage:.1f}% ({confidence_level})

┌─────────────────────────────────────────────────────────────────────────────┐
│ DETAILED COMPONENT ANALYSIS                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─ COGNITIVE TEST ANALYSIS ──────────────────────────────────────────────┐
  │                                                                          │
  │  Cognitive Risk Score:    {cognitive_risk}%                                      │
  │                                                                          │
  │  Components Evaluated:                                                   │
  │    • Word Unscrambling Test    - Language & Memory Assessment           │
  │    • Memory Pattern Test       - Working Memory & Recall                │
  │    • Reaction Time Test        - Processing Speed                       │
  │                                                                          │
  │  Risk Interpretation:                                                    │
"""
    
    # Add cognitive risk interpretation
    report += f"  │    {interpret_risk_level(cognitive_risk, 'cognitive')}\n"
    report += "  │                                                                          │\n"
    report += "  └──────────────────────────────────────────────────────────────────────┘\n\n"
    
    # Add speech analysis section if available
    if speech_analyzed and speech_risk is not None:
        report += f"""  ┌─ SPEECH ANALYSIS ──────────────────────────────────────────────────────┐
  │                                                                          │
  │  Speech Risk Score:       {speech_risk}%                                        │
  │                                                                          │
  │  Features Analyzed:                                                      │
  │    • Voice Quality (MFCCs)         - Vocal characteristics              │
  │    • Pitch Variation               - Speech patterns                    │
  │    • Speech Rate & Pauses          - Fluency indicators                 │
  │    • Spectral Features             - Voice stability                    │
  │                                                                          │
  │  Risk Interpretation:                                                    │
"""
        report += f"  │    {interpret_risk_level(speech_risk, 'speech')}\n"
        report += "  │                                                                          │\n"
        report += "  └──────────────────────────────────────────────────────────────────────┘\n\n"
    else:
        report += """  ┌─ SPEECH ANALYSIS ──────────────────────────────────────────────────────┐
  │                                                                          │
  │  Status:                  NOT PERFORMED                                  │
  │  Note:                    No audio sample was provided for analysis      │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────┘

"""
    
    # Add calculation methodology
    report += f"""┌─────────────────────────────────────────────────────────────────────────────┐
│ RISK CALCULATION METHODOLOGY                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  Overall Risk Score Calculation:
  ────────────────────────────────
"""
    
    if speech_analyzed and speech_risk is not None:
        report += f"""  
  Formula: (Cognitive Risk × 0.70) + (Speech Risk × 0.30)
  
  Calculation:
    • Cognitive Component:  {cognitive_risk}% × 70% = {cognitive_risk * 0.70:.1f}
    • Speech Component:     {speech_risk}% × 30% = {speech_risk * 0.30:.1f}
    • Combined Total:                          = {risk_score}%
  
  Weighting Rationale:
    Cognitive tests (70%) - Primary indicator of cognitive function
    Speech analysis (30%) - Supporting indicator for communication patterns
"""
    else:
        report += f"""
  Formula: Cognitive Risk Score (no speech analysis available)
  
  Calculation:
    • Cognitive Component:  {cognitive_risk}% × 100% = {cognitive_risk:.1f}%
    • Final Risk Score:                            = {risk_score}%
  
  Note: Risk based solely on cognitive tests as speech analysis was not performed.
"""
    
    # Add confidence analysis
    report += f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL CONFIDENCE ANALYSIS                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

  Confidence Score:         {confidence_percentage:.1f}%
  Confidence Level:         {confidence_level}
  
  Confidence Interpretation:
    {interpret_confidence(confidence_percentage)}

"""
    
    # Add detailed insights if available
    if insights:
        report += f"""┌─────────────────────────────────────────────────────────────────────────────┐
│ DETAILED CLINICAL INSIGHTS                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  Overall Assessment:
    {insights.get('overall_assessment', 'Assessment completed successfully.')}
  
  Cognitive Evaluation:
    {insights.get('cognitive_assessment', 'Cognitive tests completed.')}
"""
        
        if speech_analyzed:
            report += f"""  
  Speech Evaluation:
    {insights.get('speech_assessment', 'Speech analysis completed.')}
"""
        
        # Add key concerns if present
        key_concerns = insights.get('key_concerns', [])
        if key_concerns:
            report += "\n  ⚠ Key Concerns Identified:\n"
            for concern in key_concerns:
                report += f"    • {concern}\n"
        
        # Add positive indicators if present
        positive_indicators = insights.get('positive_indicators', [])
        if positive_indicators:
            report += "\n  ✓ Positive Indicators:\n"
            for indicator in positive_indicators:
                report += f"    • {indicator}\n"
        
        report += "\n"
    
    # Add recommendations section
    report += f"""┌─────────────────────────────────────────────────────────────────────────────┐
│ CLINICAL RECOMMENDATIONS                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

"""
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report += f"  {i}. {rec}\n"
    else:
        report += "  • Continue regular cognitive health monitoring\n"
        report += "  • Maintain healthy lifestyle practices\n"
    
    # Add risk category breakdown
    report += f"""

┌─────────────────────────────────────────────────────────────────────────────┐
│ RISK CATEGORY REFERENCE GUIDE                                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ✓ LOW RISK (0-29%):
    Cognitive function appears to be within normal range. Continue healthy
    lifestyle practices and annual check-ups.
  
  ⚠ MODERATE RISK (30-59%):
    Some cognitive variations detected that warrant monitoring and follow-up.
    Consider consultation with healthcare provider.
  
  🔴 HIGH RISK (60-100%):
    Significant cognitive concerns detected. Professional medical evaluation
    is strongly recommended. Schedule appointment with specialist.
  
  Your Result: {risk_category} ({risk_score}%)

┌─────────────────────────────────────────────────────────────────────────────┐
│ IMPORTANT MEDICAL DISCLAIMER                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ⚠ SCREENING TOOL ONLY - NOT A MEDICAL DIAGNOSIS
  
  This assessment is a preliminary screening tool utilizing machine learning
  algorithms to identify potential cognitive health concerns. This report does
  NOT constitute a medical diagnosis and should NOT be used as the sole basis
  for medical decisions.
  
  IMPORTANT NOTES:
  • Results should be discussed with a qualified healthcare professional
  • False positives and false negatives are possible with any screening tool
  • Temporary factors (stress, fatigue, illness) can affect test performance
  • Comprehensive medical evaluation is required for accurate diagnosis
  • This tool is designed to identify individuals who may benefit from
    professional evaluation, not to replace clinical assessment
  
  NEXT STEPS:
  • Share this report with your primary care physician
  • Schedule a comprehensive cognitive evaluation if recommended
  • Do not make medical decisions based solely on this screening
  • Maintain regular health check-ups regardless of screening results

╔══════════════════════════════════════════════════════════════════════════════╗
║                           END OF REPORT                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝


"""
    
    return report


# ==================== HELPER FUNCTIONS ====================

def get_risk_emoji(risk_category):
    """Get emoji for risk category"""
    if "Low" in risk_category:
        return "✅"
    elif "Moderate" in risk_category:
        return "⚠️"
    else:
        return "🔴"

def get_confidence_level(confidence_percentage):
    """Get confidence level description"""
    if confidence_percentage >= 90:
        return "Very High"
    elif confidence_percentage >= 75:
        return "High"
    elif confidence_percentage >= 60:
        return "Moderate"
    elif confidence_percentage >= 40:
        return "Low"
    else:
        return "Very Low"

def interpret_risk_level(risk_score, component_type):
    """Generate risk interpretation text"""
    if risk_score < 30:
        return f"Low risk detected in {component_type} assessment. Performance is within normal range."
    elif risk_score < 60:
        return f"Moderate risk detected in {component_type} assessment. Monitoring recommended."
    else:
        return f"High risk detected in {component_type} assessment. Professional evaluation advised."

def interpret_confidence(confidence_percentage):
    """Generate confidence interpretation"""
    if confidence_percentage >= 85:
        return "The model has high confidence in this prediction. Results are considered reliable."
    elif confidence_percentage >= 70:
        return "The model has moderate confidence in this prediction. Results should be interpreted with clinical judgment."
    else:
        return "The model has low confidence in this prediction. Consider retaking assessment or consulting professional evaluation."


def append_to_google_docs(service, content):
    """
    Append text content to the end of a Google Docs document
    
    Args:
        service: Google Docs API service object
        content (str): Text content to append
    """
    try:
        # Step 1: Get the current document to find the end index
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Step 2: Get the index of the last position in the document
        end_index = document.get('body').get('content')[-1].get('endIndex') - 1
        
        # Step 3: Create the insert request
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': end_index
                    },
                    'text': content
                }
            }
        ]
        
        # Step 4: Execute the batch update to append content
        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        
        print(f"✓ Successfully appended comprehensive report to Google Docs")
        return result
        
    except HttpError as error:
        print(f"✗ An error occurred: {error}")
        raise


# ==================== MAIN FUNCTION FOR TESTING ====================

def main():
    """
    Main function for testing the comprehensive report generation
    """
    print("\n" + "="*80)
    print(" " * 20 + "COMPREHENSIVE REPORT GENERATOR - TEST")
    print("="*80 + "\n")
    
    # Check if service account file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"✗ Error: '{SERVICE_ACCOUNT_FILE}' not found!")
        print("\nSetup Instructions:")
        print("1. Create a Google Cloud Project")
        print("2. Enable Google Docs API")
        print("3. Create a Service Account")
        print("4. Download JSON key as 'service_account.json'")
        print("5. Share your Google Doc with the service account email")
        return
    
    # Check if document ID is set
    if DOCUMENT_ID == "your-document-id-here":
        print("✗ Error: Please set DOCUMENT_ID variable!")
        print("\nHow to get Document ID:")
        print("1. Open your Google Doc")
        print("2. Copy ID from URL: docs.google.com/document/d/{DOCUMENT_ID}/edit")
        print("3. Set DOCUMENT_ID variable in this file")
        return
    
    # Test with comprehensive sample data
    print("Testing with comprehensive patient data...\n")
    
    # Example: Complete analysis with all details
    comprehensive_result = {
        "patient_id": "P8F4A2C",
        "risk_score": 42,
        "risk_category": "Moderate Risk",
        "cognitive_risk": 48,
        "speech_risk": 35,
        "speech_analyzed": True,
        "confidence_score": 0.85,
        "recommendations": [
            "Schedule a consultation with your healthcare provider for comprehensive evaluation",
            "Increase cognitive exercises and brain training activities",
            "Monitor changes in memory or cognitive function over the next 3-6 months",
            "Consider lifestyle modifications including diet, exercise, and sleep hygiene"
        ],
        "insights": {
            "overall_assessment": "Moderate risk detected. Some cognitive variations have been identified that warrant monitoring and professional follow-up.",
            "cognitive_assessment": "Cognitive test results show some areas that may benefit from attention and continued monitoring over time.",
            "speech_assessment": "Speech patterns show some characteristics that may warrant further evaluation.",
            "key_concerns": [
                "Memory performance below optimal range",
                "Reaction time slightly elevated"
            ],
            "positive_indicators": [
                "Strong word recognition abilities",
                "Good overall cognitive reserve"
            ]
        }
    }
    
    # Generate comprehensive report
    try:
        print("Generating comprehensive report...")
        generate_data(comprehensive_result)
        print()
        
        print("="*80)
        print("✓ Comprehensive test report generated successfully!")
        print(f"✓ Check your Google Doc: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
        print("="*80 + "\n")
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"✗ Test failed: {e}")
        print("="*80 + "\n")


if __name__ == "__main__":
    main()