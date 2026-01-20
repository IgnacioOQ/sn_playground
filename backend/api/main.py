"""
FastAPI Application Entry Point

Main application with CORS configuration and route mounting.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router


# Create FastAPI app
app = FastAPI(
    title="Iterated Prisoners Dilemma",
    description="Backend for the iterated prisoners dilemma simulation",
    version="1.0.0"
)

# Configure CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(router)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "name": "Iterated Prisoners Dilemma API",
        "version": "1.0.0",
        "docs": "/docs"
    }
