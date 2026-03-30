"""
Service Provider Service - Microservice for managing service providers
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

# Import routes
try:
    from app.routes import router
    logger.info("Routes imported successfully")
except Exception as e:
    logger.error(f"Failed to import routes: {e}")
    router = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    logger.info("Service Provider Service started")
    logger.info("Service URLs configured - Ready to accept requests")
    yield
    logger.info("Service Provider Service shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Service Provider Service",
    description="Microservice for managing service providers",
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

# Include routes if available
if router:
    app.include_router(router)
    logger.info("Routes included in application")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Service status"""
    return {
        "status": "running",
        "service": "Service Provider Service",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "service-provider-service"
    }


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    host = os.getenv("SERVICE_PROVIDER_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", 8002))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Service Provider Service on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )