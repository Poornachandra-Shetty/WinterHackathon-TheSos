"""
Main FastAPI Application
Entry point for Dementia Screening API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router
from ai.model import load_model

# Initialize FastAPI app
app = FastAPI(
    title="Dementia Screening API",
    description="AI-powered dementia risk assessment API",
    version="1.0.0"
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
    print("Starting Dementia Screening API...")
    load_model()
    print("✓ Server ready")

# Include API routes
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Dementia Screening API",
        "version": "1.0.0",
        "status": "active",
        "documentation": "/docs",
        "health_check": "/health",
        "endpoints": {
            "analyze": "/api/analyze",
            "test": "/api/test"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "dementia-screening-api",
        "version": "1.0.0"
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