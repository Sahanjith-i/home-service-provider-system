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


# ============================================================================
# BOOKING ENDPOINTS
# ============================================================================

# TODO: Integrate with app.database for MongoDB operations
# TODO: Implement booking routes using app.routes

@app.post("/bookings", tags=["Bookings"])
async def create_booking(booking_data: dict):
    """Create a new booking"""
    return {
        "message": "Booking created successfully",
        "booking": booking_data
    }


@app.get("/bookings", tags=["Bookings"])
async def get_all_bookings():
    """Get all bookings"""
    return {
        "bookings": []
    }


@app.get("/bookings/{booking_id}", tags=["Bookings"])
async def get_booking(booking_id: int):
    """Get a specific booking by ID"""
    return {
        "booking_id": booking_id,
        "message": "Booking retrieved"
    }


@app.put("/bookings/{booking_id}", tags=["Bookings"])
async def update_booking(booking_id: int, booking_data: dict):
    """Update a booking"""
    return {
        "message": "Booking updated successfully",
        "booking_id": booking_id,
        "booking": booking_data
    }


@app.patch("/bookings/{booking_id}/status", tags=["Bookings"])
async def update_booking_status(booking_id: int, status: str):
    """Update booking status"""
    return {
        "message": "Booking status updated successfully",
        "booking_id": booking_id,
        "status": status
    }


@app.delete("/bookings/{booking_id}", tags=["Bookings"])
async def delete_booking(booking_id: int):
    """Delete a booking"""
    return {
        "message": "Booking deleted successfully",
        "booking_id": booking_id
    }


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
