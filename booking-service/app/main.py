"""
Booking Service - Microservice for managing bookings
"""

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import router as booking_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    logger.info("Booking Service started")
    yield
    logger.info("Booking Service shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Booking Service",
    description="Microservice for managing service bookings",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Service status"""
    return {
        "status": "running",
        "service": "Booking Service",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "booking-service"
    }


# Include booking CRUD routes backed by MongoDB
app.include_router(booking_router, tags=["Bookings"])


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    host = os.getenv("BOOKING_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", 8003))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Booking Service on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
