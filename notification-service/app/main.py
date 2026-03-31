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


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "service": "Notification Service",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "notification-service"
    }

# Include routes
from app.routes import router as notification_router
app.include_router(notification_router, prefix="/api", tags=["Notifications"])


if __name__ == "__main__":
    host = os.getenv("NOTIFICATION_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", 8004))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Notification Service on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
