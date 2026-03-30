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


# ============================================================================
# CUSTOMER ENDPOINTS
# ============================================================================

# TODO: Integrate with app.database for MongoDB operations
# TODO: Implement customer routes using app.routes

@app.post("/customers", tags=["Customers"])
async def create_customer(customer_data: dict):
    """Create a new customer"""
    return {
        "message": "Customer created successfully",
        "customer": customer_data
    }


@app.get("/customers", tags=["Customers"])
async def get_all_customers():
    """Get all customers"""
    return {
        "customers": []
    }


@app.get("/customers/{customer_id}", tags=["Customers"])
async def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    return {
        "customer_id": customer_id,
        "message": "Customer retrieved"
    }


@app.put("/customers/{customer_id}", tags=["Customers"])
async def update_customer(customer_id: int, customer_data: dict):
    """Update a customer"""
    return {
        "message": "Customer updated successfully",
        "customer_id": customer_id,
        "customer": customer_data
    }


@app.delete("/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int):
    """Delete a customer"""
    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id
    }


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
