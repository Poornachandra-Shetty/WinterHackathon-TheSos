from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys
# Ensure the project root is on sys.path so top-level packages (e.g., `routes`) can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent))
from routes.analyze import router as analyze_router

# Create FastAPI application instance
app = FastAPI(
    title="Dementia Screening API",
    description="AI-powered cognitive assessment backend",
    version="1.0.0"
)

# Configure CORS to allow React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include API routes with /api prefix
app.include_router(analyze_router, prefix="/api")

# Root endpoint to verify backend is running
@app.get("/")
def read_root():
    return {
        "message": "Dementia Screening API is running",
        "status": "active",
        "version": "1.0.0"
    }