"""
Notification Service - Microservice for managing notifications
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
    logger.info("Notification Service started")
    yield
    logger.info("Notification Service shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Notification Service",
    description="Microservice for managing notifications",
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
        "service": "Notification Service",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "notification-service"
    }


# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

# TODO: Integrate with app.database for MongoDB operations
# TODO: Implement notification routes using app.routes

@app.post("/notifications", tags=["Notifications"])
async def send_notification(notification_data: dict):
    """Send a notification"""
    return {
        "message": "Notification sent successfully",
        "notification": notification_data
    }


@app.get("/notifications", tags=["Notifications"])
async def get_all_notifications():
    """Get all notifications"""
    return {
        "notifications": []
    }


@app.get("/notifications/{notification_id}", tags=["Notifications"])
async def get_notification(notification_id: int):
    """Get a specific notification by ID"""
    return {
        "notification_id": notification_id,
        "message": "Notification retrieved"
    }


@app.delete("/notifications/{notification_id}", tags=["Notifications"])
async def delete_notification(notification_id: int):
    """Delete a notification"""
    return {
        "message": "Notification deleted successfully",
        "notification_id": notification_id
    }


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    host = os.getenv("NOTIFICATION_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", 8004))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Notification Service on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
