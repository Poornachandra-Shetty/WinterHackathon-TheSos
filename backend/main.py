"""
Main FastAPI Application
Entry point for Dementia Screening API with Survey Module
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router
from ai.model import load_model
from generate_report import generate_data

result = {
    "patient_id": "P12345",
    "prediction": "Moderate Risk",
    "confidence": 72.5
}

generate_data(result)
# Initialize FastAPI app
app = FastAPI(
    title="Dementia Screening API",
    description="AI-powered dementia risk assessment API with contextual survey adjustments",
    version="2.0.0"
)

# Configure CORS - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models on startup
@app.on_event("startup")
async def startup_event():
    """Load ML models when server starts"""
    print("=" * 60)
    print("Starting Dementia Screening API v2.0...")
    print("=" * 60)
    load_model()
    print("✓ ML Models loaded")
    print("✓ Survey module initialized")
    print("✓ Server ready")
    print("=" * 60)
    print("\n📋 New Features:")
    print("  • Contextual survey integration")
    print("  • False positive reduction")
    print("  • Confidence scoring")
    print("  • Bias-aware adjustments")
    print("\n🔗 Endpoints:")
    print("  • POST /api/analyze - Full analysis with survey")
    print("  • GET /docs - API documentation")
    print("  • GET /health - Health check")
    print("=" * 60 + "\n")

# Include API routes
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Dementia Screening API with Survey Module",
        "version": "2.0.0",
        "status": "active",
        "documentation": "/docs",
        "health_check": "/health",
        "features": {
            "cognitive_assessment": "Word, Memory, Reaction time tests",
            "speech_analysis": "Optional audio analysis",
            "survey_module": "10-question contextual survey",
            "false_positive_reduction": "Adjusts for sleep, stress, environment",
            "confidence_scoring": "Reliability assessment (0-100%)",
            "bias_mitigation": "Age, education, digital familiarity adjustments"
        },
        "endpoints": {
            "analyze": {
                "url": "/api/analyze",
                "method": "POST",
                "description": "Complete analysis with cognitive tests + survey",
                "accepts": [
                    "word_test_score (float)",
                    "memory_test_score (float)",
                    "reaction_time (float)",
                    "reaction_test_score (float, optional)",
                    "sleep (str)",
                    "stress (str)",
                    "age_range (str)",
                    "environment (str)",
                    "fatigue (str)",
                    "digital_familiarity (str)",
                    "focus (str)",
                    "health (str)",
                    "education (str)",
                    "retake (str)",
                    "audio (file, optional)"
                ],
                "returns": {
                    "risk_score": "Original cognitive risk (0-100)",
                    "adjusted_risk_score": "Survey-adjusted risk (0-100)",
                    "risk_category": "Low/Moderate/High Risk",
                    "confidence_score": "Assessment reliability (0-100%)",
                    "confidence_level": "High/Medium/Low",
                    "survey_flags": "List of contextual factors",
                    "recommendation": "Actionable next steps",
                    "speech_analyzed": "Boolean",
                    "interpretation": "Human-readable summary"
                }
            },
            "test": "/api/test"
        },
        "survey_guarantees": [
            "NEVER increases risk score",
            "Can only reduce risk or lower confidence",
            "Cognitive tests remain primary signal",
            "All adjustments are transparent and justified"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "dementia-screening-api",
        "version": "2.0.0",
        "features_enabled": {
            "cognitive_assessment": True,
            "speech_analysis": True,
            "survey_module": True,
            "false_positive_reduction": True,
            "confidence_scoring": True
        },
        "survey_questions": 10,
        "risk_reduction_range": "0-30%",
        "confidence_range": "50-95%"
    }

@app.get("/api/survey-info")
async def survey_info():
    """Information about the survey module"""
    return {
        "survey_version": "1.0.0",
        "total_questions": 10,
        "purpose": "Reduce false positives and adjust confidence",
        "questions": [
            {
                "id": "sleep",
                "question": "How many hours did you sleep last night?",
                "purpose": "Sleep deprivation can mimic cognitive impairment",
                "options": ["less_than_4", "4-6", "6-8", "more_than_8"]
            },
            {
                "id": "stress",
                "question": "How stressed do you feel right now?",
                "purpose": "Stress slows reaction time and memory",
                "options": ["low", "moderate", "high"]
            },
            {
                "id": "age_range",
                "question": "What is your age range?",
                "purpose": "Prevents unfairly flagging healthy older users",
                "options": ["18-30", "31-45", "46-60", "60+"]
            },
            {
                "id": "environment",
                "question": "What best describes your current environment?",
                "purpose": "Attention tests fail under distractions",
                "options": ["quiet", "some_noise", "distracting"]
            },
            {
                "id": "fatigue",
                "question": "How mentally tired do you feel today?",
                "purpose": "Mental fatigue mimics memory problems",
                "options": ["fresh", "slightly_tired", "very_tired"]
            },
            {
                "id": "digital_familiarity",
                "question": "How often do you play digital games or use interactive apps?",
                "purpose": "Prevents misinterpreting unfamiliarity as slow cognition",
                "options": ["often", "occasionally", "rare"]
            },
            {
                "id": "focus",
                "question": "How focused do you feel at this moment?",
                "purpose": "Used to lower confidence, never increase risk",
                "options": ["fully_focused", "somewhat_distracted", "very_distracted"]
            },
            {
                "id": "health",
                "question": "Are you currently feeling unwell (fever, headache, pain)?",
                "purpose": "Avoids false positives during illness",
                "options": ["no", "mild_discomfort", "significant_discomfort"]
            },
            {
                "id": "education",
                "question": "Highest level of education completed?",
                "purpose": "Fairness calibration only (low weight)",
                "options": ["school", "undergraduate", "postgraduate"]
            },
            {
                "id": "retake",
                "question": "Would you be willing to retake this screening under better conditions?",
                "purpose": "Used only for confidence score",
                "options": ["yes", "maybe", "not_sure"]
            }
        ],
        "scoring_principles": [
            "Survey NEVER increases risk score",
            "Survey can reduce risk by 0-30%",
            "Confidence ranges from 50-95%",
            "Multiple suboptimal factors compound adjustments",
            "Optimal conditions result in minimal adjustment"
        ]
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )