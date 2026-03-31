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

from .schemas import (
    BookingCreateRequest,
    BookingUpdateRequest,
    LoginCustomerRequest,
    NotificationRequest,
    RegisterCustomerRequest,
    ServiceProviderCreateRequest,
    ServiceProviderUpdateRequest,
    UpdateCustomerRequest,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SERVICE_URLS = {
    "booking-service": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8003"),
    "customer-service": os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8001"),
    "service-provider-service": os.getenv("SERVICE_PROVIDER_URL", "http://localhost:8002"),
    "notification-service": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004"),
}

http_client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("API Gateway started")
    logger.info(f"Service URLs: {SERVICE_URLS}")
    yield
    await http_client.aclose()
    logger.info("API Gateway shutdown")


app = FastAPI(
    title="Home Service Provider API Gateway",
    description="API Gateway for routing requests to microservices",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def proxy_request(
    service_name: str,
    method: str,
    path: str,
    body: Optional[dict] = None,
    params: Optional[dict] = None
):
    if service_name not in SERVICE_URLS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_name}' not found"
        )

    service_url = SERVICE_URLS[service_name]
    full_url = f"{service_url}{path}"

    try:
        logger.info(f"Proxying {method} request to {full_url}")

        response = await http_client.request(
            method=method,
            url=full_url,
            json=body,
            params=params
        )

        logger.info(f"{service_name} responded with {response.status_code}")

        content_type = response.headers.get("content-type", "")

        if response.status_code >= 400:
            detail = None
            try:
                detail = response.json()
            except Exception:
                detail = response.text

            raise HTTPException(
                status_code=response.status_code,
                detail=detail
            )

        if "application/json" in content_type:
            return response.json()

        return {"message": response.text}

    except httpx.RequestError as e:
        logger.error(f"{service_name} unavailable: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Service '{service_name}' is unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected gateway error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Internal gateway error"
        )


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "application": "Home Service Provider API Gateway",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "gateway": "running"
    }


@app.get("/health/services", tags=["Health"])
async def services_health():
    health_status = {}

    for service_name, service_url in SERVICE_URLS.items():
        try:
            # try /health first
            response = await http_client.get(f"{service_url}/health", timeout=5.0)

            health_status[service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "url": service_url
            }
        except Exception:
            try:
                # fallback to root endpoint
                response = await http_client.get(f"{service_url}/", timeout=5.0)

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
# SERVICE PROVIDER ROUTES
# ============================================================================

@app.post("/api/providers", tags=["Service Providers"])
async def create_provider(provider_data: ServiceProviderCreateRequest):
    return await proxy_request(
        "service-provider-service",
        "POST",
        "/providers",
        body=provider_data.model_dump(mode="json")
    )


@app.get("/api/providers", tags=["Service Providers"])
async def get_all_providers():
    return await proxy_request("service-provider-service", "GET", "/providers")


@app.get("/api/providers/{provider_id}", tags=["Service Providers"])
async def get_provider(provider_id: int):
    return await proxy_request("service-provider-service", "GET", f"/providers/{provider_id}")


@app.put("/api/providers/{provider_id}", tags=["Service Providers"])
async def update_provider(provider_id: int, provider_data: ServiceProviderUpdateRequest):
    return await proxy_request(
        "service-provider-service",
        "PUT",
        f"/providers/{provider_id}",
        body=provider_data.model_dump(mode="json")
    )


@app.patch("/api/providers/{provider_id}/phone", tags=["Service Providers"])
async def update_provider_phone(provider_id: int, phone: str):
    return await proxy_request(
        "service-provider-service",
        "PATCH",
        f"/providers/{provider_id}/phone",
        params={"phone": phone}
    )


@app.delete("/api/providers/{provider_id}", tags=["Service Providers"])
async def delete_provider(provider_id: int):
    return await proxy_request("service-provider-service", "DELETE", f"/providers/{provider_id}")


# ============================================================================
# BOOKING ROUTES
# booking_id should be str because booking service uses IDs like B0001
# ============================================================================

@app.post("/api/bookings", tags=["Bookings"])
async def create_booking(booking_data: BookingCreateRequest):
    return await proxy_request(
        "booking-service",
        "POST",
        "/bookings",
        body=booking_data.model_dump(mode="json")
    )


@app.get("/api/bookings", tags=["Bookings"])
async def get_all_bookings():
    return await proxy_request("booking-service", "GET", "/bookings")


@app.get("/api/bookings/{booking_id}", tags=["Bookings"])
async def get_booking(booking_id: str):
    return await proxy_request("booking-service", "GET", f"/bookings/{booking_id}")


@app.put("/api/bookings/{booking_id}", tags=["Bookings"])
async def update_booking(booking_id: str, booking_data: BookingUpdateRequest):
    return await proxy_request(
        "booking-service",
        "PUT",
        f"/bookings/{booking_id}",
        body=booking_data.model_dump(mode="json")
    )


@app.patch("/api/bookings/{booking_id}/status", tags=["Bookings"])
async def update_booking_status(booking_id: str, status: str):
    return await proxy_request(
        "booking-service",
        "PATCH",
        f"/bookings/{booking_id}/status",
        params={"status": status}
    )


@app.delete("/api/bookings/{booking_id}", tags=["Bookings"])
async def delete_booking(booking_id: str):
    return await proxy_request("booking-service", "DELETE", f"/bookings/{booking_id}")


# ============================================================================
# CUSTOMER ROUTES
# customer service has /customers/register and /customers/login too
# customer_id should be str
# ============================================================================

@app.post("/api/customers/register", tags=["Customers"])
async def register_customer(customer_data: RegisterCustomerRequest):
    return await proxy_request(
        "customer-service",
        "POST",
        "/customers/register",
        body=customer_data.model_dump(mode="json")
    )


@app.post("/api/customers/login", tags=["Customers"])
async def login_customer(login_data: LoginCustomerRequest):
    return await proxy_request(
        "customer-service",
        "POST",
        "/customers/login",
        body=login_data.model_dump(mode="json")
    )


@app.post("/api/customers", tags=["Customers"])
async def create_customer(customer_data: RegisterCustomerRequest):
    return await proxy_request(
        "customer-service",
        "POST",
        "/customers",
        body=customer_data.model_dump(mode="json")
    )


@app.get("/api/customers", tags=["Customers"])
async def get_all_customers(skip: int = 0, limit: int = 10):
    return await proxy_request(
        "customer-service",
        "GET",
        "/customers",
        params={"skip": skip, "limit": limit}
    )


@app.get("/api/customers/{customer_id}", tags=["Customers"])
async def get_customer(customer_id: str):
    return await proxy_request("customer-service", "GET", f"/customers/{customer_id}")


@app.put("/api/customers/{customer_id}", tags=["Customers"])
async def update_customer(customer_id: str, customer_data: UpdateCustomerRequest):
    return await proxy_request(
        "customer-service",
        "PUT",
        f"/customers/{customer_id}",
        body=customer_data.model_dump(mode="json")
    )


@app.delete("/api/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: str):
    return await proxy_request("customer-service", "DELETE", f"/customers/{customer_id}")


# ============================================================================
# NOTIFICATION ROUTES
# notification service is mounted with prefix="/api"
# so gateway must call /api/notifications internally
# notification_id should be str like N0001
# ============================================================================

@app.post("/api/notifications", tags=["Notifications"])
async def send_notification(notification_data: NotificationRequest):
    return await proxy_request(
        "notification-service",
        "POST",
        "/api/notifications",
        body=notification_data.model_dump(mode="json")
    )


@app.get("/api/notifications", tags=["Notifications"])
async def get_all_notifications():
    return await proxy_request("notification-service", "GET", "/api/notifications")


@app.get("/api/notifications/{notification_id}", tags=["Notifications"])
async def get_notification(notification_id: str):
    return await proxy_request("notification-service", "GET", f"/api/notifications/{notification_id}")


@app.put("/api/notifications/{notification_id}", tags=["Notifications"])
async def update_notification(notification_id: str, notification_data: NotificationRequest):
    return await proxy_request(
        "notification-service",
        "PUT",
        f"/api/notifications/{notification_id}",
        body=notification_data.model_dump(mode="json")
    )


@app.patch("/api/notifications/{notification_id}/read", tags=["Notifications"])
async def mark_notification_as_read(notification_id: str):
    return await proxy_request("notification-service", "PATCH", f"/api/notifications/{notification_id}/read")


@app.delete("/api/notifications/{notification_id}", tags=["Notifications"])
async def delete_notification(notification_id: str):
    return await proxy_request("notification-service", "DELETE", f"/api/notifications/{notification_id}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "status_code": 500,
            "detail": "An unexpected error occurred"
        },
    )


if __name__ == "__main__":
    host = os.getenv("API_GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("API_GATEWAY_PORT", 8000))
    reload = os.getenv("DEBUG", "False").lower() == "true"

    logger.info(f"Starting API Gateway on {host}:{port}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )