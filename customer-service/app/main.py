"""
Customer Service - Microservice for managing customers
"""

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .routes import router as customer_router

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
    logger.info("Customer Service started")
    yield
    logger.info("Customer Service shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Customer Service",
    description="Microservice for managing customers",
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
        "service": "Customer Service",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "customer-service"
    }


# Include customer auth/profile routes backed by MongoDB
app.include_router(customer_router)


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    host = os.getenv("CUSTOMER_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", 8001))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Customer Service on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
