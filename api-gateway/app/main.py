"""
API Gateway for Home Service Provider System
Routes requests to appropriate microservices and provides unified API interface
"""

import os
import httpx
import logging
from contextlib import asynccontextmanager
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
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

# Service URLs from environment variables
SERVICE_URLS = {
    "booking-service": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8003"),
    "customer-service": os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8001"),
    "service-provider-service": os.getenv("SERVICE_PROVIDER_URL", "http://localhost:8002"),
    "notification-service": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004"),
}

# Global HTTP client
http_client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - initialize and cleanup HTTP client
    """
    global http_client
    # Startup
    http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("API Gateway started - HTTP client initialized")
    logger.info(f"Service URLs: {SERVICE_URLS}")
    
    yield
    
    # Shutdown
    await http_client.aclose()
    logger.info("API Gateway shutdown - HTTP client closed")


# Initialize FastAPI app
app = FastAPI(
    title="Home Service Provider API Gateway",
    description="API Gateway for routing requests to microservices",
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
# UTILITY FUNCTIONS
# ============================================================================

async def proxy_request(
    service_name: str,
    method: str,
    path: str,
    body: Optional[dict] = None,
    params: Optional[dict] = None
) -> dict:
    """
    Proxy request to the specified microservice
    
    Args:
        service_name: Name of the service (must exist in SERVICE_URLS)
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        path: Request path (without service URL)
        body: Request body for POST/PUT/PATCH requests
        params: Query parameters
    
    Returns:
        Response JSON from the service
    
    Raises:
        HTTPException: If service is unavailable or request fails
    """
    if service_name not in SERVICE_URLS:
        logger.error(f"Unknown service: {service_name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_name}' not found"
        )
    
    service_url = SERVICE_URLS[service_name]
    full_url = f"{service_url}{path}"
    
    try:
        logger.info(f"Proxying {method} request to {service_name}: {path}")
        
        response = await http_client.request(
            method=method,
            url=full_url,
            json=body,
            params=params
        )
        
        # Log response status
        logger.info(f"{service_name} responded with status {response.status_code}")
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.json()
    
    except httpx.HTTPError as e:
        error_message = f"Service '{service_name}' error: {str(e)}"
        logger.error(error_message)
        
        if isinstance(e, httpx.HTTPStatusError):
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e.response.json()) if e.response.text else str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Service '{service_name}' is unavailable"
            )
    
    except Exception as e:
        error_message = f"Unexpected error while calling '{service_name}': {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Internal gateway error"
        )


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API Gateway status"""
    return {
        "status": "running",
        "application": "Home Service Provider API Gateway",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for the API Gateway"""
    return {
        "status": "healthy",
        "gateway": "running"
    }


@app.get("/health/services", tags=["Health"])
async def services_health():
    """Check health of all microservices"""
    health_status = {}
    
    for service_name, service_url in SERVICE_URLS.items():
        try:
            response = await http_client.get(f"{service_url}/health", timeout=5.0)
            health_status[service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "url": service_url
            }
        except Exception as e:
            health_status[service_name] = {
                "status": "unavailable",
                "url": service_url,
                "error": str(e)
            }
    
    return health_status


# ============================================================================
# SERVICE PROVIDER ROUTES (Proxy to service-provider-service)
# ============================================================================

@app.post("/api/providers", tags=["Service Providers"])
async def create_provider(provider_data: dict):
    """Create a new service provider"""
    return await proxy_request("service-provider-service", "POST", "/providers", body=provider_data)


@app.get("/api/providers", tags=["Service Providers"])
async def get_all_providers():
    """Get all service providers"""
    return await proxy_request("service-provider-service", "GET", "/providers")


@app.get("/api/providers/{provider_id}", tags=["Service Providers"])
async def get_provider(provider_id: int):
    """Get a specific service provider by ID"""
    return await proxy_request("service-provider-service", "GET", f"/providers/{provider_id}")


@app.put("/api/providers/{provider_id}", tags=["Service Providers"])
async def update_provider(provider_id: int, provider_data: dict):
    """Update a service provider"""
    return await proxy_request("service-provider-service", "PUT", f"/providers/{provider_id}", body=provider_data)


@app.patch("/api/providers/{provider_id}/phone", tags=["Service Providers"])
async def update_provider_phone(provider_id: int, phone: str):
    """Update service provider's phone number"""
    return await proxy_request("service-provider-service", "PATCH", f"/providers/{provider_id}/phone", params={"phone": phone})


@app.delete("/api/providers/{provider_id}", tags=["Service Providers"])
async def delete_provider(provider_id: int):
    """Delete a service provider"""
    return await proxy_request("service-provider-service", "DELETE", f"/providers/{provider_id}")


# ============================================================================
# BOOKING ROUTES (Proxy to booking-service)
# ============================================================================

@app.post("/api/bookings", tags=["Bookings"])
async def create_booking(booking_data: dict):
    """Create a new booking"""
    return await proxy_request("booking-service", "POST", "/bookings", body=booking_data)


@app.get("/api/bookings", tags=["Bookings"])
async def get_all_bookings():
    """Get all bookings"""
    return await proxy_request("booking-service", "GET", "/bookings")


@app.get("/api/bookings/{booking_id}", tags=["Bookings"])
async def get_booking(booking_id: int):
    """Get a specific booking by ID"""
    return await proxy_request("booking-service", "GET", f"/bookings/{booking_id}")


@app.put("/api/bookings/{booking_id}", tags=["Bookings"])
async def update_booking(booking_id: int, booking_data: dict):
    """Update a booking"""
    return await proxy_request("booking-service", "PUT", f"/bookings/{booking_id}", body=booking_data)


@app.patch("/api/bookings/{booking_id}/status", tags=["Bookings"])
async def update_booking_status(booking_id: int, status: str):
    """Update booking status"""
    return await proxy_request("booking-service", "PATCH", f"/bookings/{booking_id}/status", body={"status": status})


@app.delete("/api/bookings/{booking_id}", tags=["Bookings"])
async def delete_booking(booking_id: int):
    """Delete a booking"""
    return await proxy_request("booking-service", "DELETE", f"/bookings/{booking_id}")


# ============================================================================
# CUSTOMER ROUTES (Proxy to customer-service)
# ============================================================================

@app.post("/api/customers", tags=["Customers"])
async def create_customer(customer_data: dict):
    """Create a new customer"""
    return await proxy_request("customer-service", "POST", "/customers", body=customer_data)


@app.get("/api/customers", tags=["Customers"])
async def get_all_customers():
    """Get all customers"""
    return await proxy_request("customer-service", "GET", "/customers")


@app.get("/api/customers/{customer_id}", tags=["Customers"])
async def get_customer(customer_id: str):
    """Get a specific customer by ID"""
    return await proxy_request("customer-service", "GET", f"/customers/{customer_id}")


@app.put("/api/customers/{customer_id}", tags=["Customers"])
async def update_customer(customer_id: str, customer_data: dict):
    """Update a customer"""
    return await proxy_request("customer-service", "PUT", f"/customers/{customer_id}", body=customer_data)


@app.delete("/api/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: str):
    """Delete a customer"""
    return await proxy_request("customer-service", "DELETE", f"/customers/{customer_id}")


# ============================================================================
# NOTIFICATION ROUTES (Proxy to notification-service)
# ============================================================================

@app.post("/api/notifications", tags=["Notifications"])
async def send_notification(notification_data: dict):
    """Send a notification"""
    return await proxy_request("notification-service", "POST", "/notifications", body=notification_data)


@app.get("/api/notifications", tags=["Notifications"])
async def get_all_notifications():
    """Get all notifications"""
    return await proxy_request("notification-service", "GET", "/notifications")


@app.get("/api/notifications/{notification_id}", tags=["Notifications"])
async def get_notification(notification_id: int):
    """Get a specific notification by ID"""
    return await proxy_request("notification-service", "GET", f"/notifications/{notification_id}")


@app.delete("/api/notifications/{notification_id}", tags=["Notifications"])
async def delete_notification(notification_id: int):
    """Delete a notification"""
    return await proxy_request("notification-service", "DELETE", f"/notifications/{notification_id}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "status_code": exc.status_code,
            "detail": exc.detail
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "status_code": 500,
            "detail": "An unexpected error occurred"
        },
    )


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("API_GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("API_GATEWAY_PORT", 8000))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting API Gateway on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
