from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from api-gateway folder
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="API Gateway", version="1.0.0")

# Service URLs
SERVICES = {
    "customer": os.getenv("CUSTOMER_SERVICE_URL"),
    "provider": os.getenv("SERVICE_PROVIDER_URL"),
    "booking": os.getenv("BOOKING_SERVICE_URL"),
    "notification": os.getenv("NOTIFICATION_SERVICE_URL")
}


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES or not SERVICES[service]:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "PATCH":
                response = await client.patch(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )

        except httpx.RequestError:
            raise HTTPException(
                status_code=503,
                detail=f"Service {service} is unavailable"
            )


@app.get("/")
def root():
    return {
        "message": "API Gateway is running",
        "available_services": list(SERVICES.keys())
    }


# ---------------- CUSTOMER SERVICE ----------------

@app.get("/gateway/customers")
async def get_all_customers():
    return await forward_request("customer", "/customers", "GET")


@app.get("/gateway/customers/{customer_id}")
async def get_customer(customer_id: int):
    return await forward_request("customer", f"/customers/{customer_id}", "GET")


@app.post("/gateway/customers")
async def create_customer(request: Request):
    json_body = await request.json()
    return await forward_request("customer", "/customers", "POST", json=json_body)


@app.put("/gateway/customers/{customer_id}")
async def update_customer(customer_id: int, request: Request):
    json_body = await request.json()
    return await forward_request("customer", f"/customers/{customer_id}", "PUT", json=json_body)


@app.delete("/gateway/customers/{customer_id}")
async def delete_customer(customer_id: int):
    return await forward_request("customer", f"/customers/{customer_id}", "DELETE")


# ---------------- SERVICE PROVIDER SERVICE ----------------

@app.get("/gateway/providers")
async def get_all_providers():
    return await forward_request("provider", "/providers", "GET")


@app.get("/gateway/providers/{provider_id}")
async def get_provider(provider_id: int):
    return await forward_request("provider", f"/providers/{provider_id}", "GET")


@app.post("/gateway/providers")
async def create_provider(request: Request):
    json_body = await request.json()
    return await forward_request("provider", "/providers", "POST", json=json_body)


@app.put("/gateway/providers/{provider_id}")
async def update_provider(provider_id: int, request: Request):
    json_body = await request.json()
    return await forward_request("provider", f"/providers/{provider_id}", "PUT", json=json_body)


@app.patch("/gateway/providers/{provider_id}/phone")
async def update_provider_phone(provider_id: int, request: Request):
    json_body = await request.json()
    return await forward_request("provider", f"/providers/{provider_id}/phone", "PATCH", json=json_body)


@app.delete("/gateway/providers/{provider_id}")
async def delete_provider(provider_id: int):
    return await forward_request("provider", f"/providers/{provider_id}", "DELETE")


# ---------------- BOOKING SERVICE ----------------

@app.get("/gateway/bookings")
async def get_all_bookings():
    return await forward_request("booking", "/bookings", "GET")


@app.get("/gateway/bookings/{booking_id}")
async def get_booking(booking_id: int):
    return await forward_request("booking", f"/bookings/{booking_id}", "GET")


@app.post("/gateway/bookings")
async def create_booking(request: Request):
    json_body = await request.json()
    return await forward_request("booking", "/bookings", "POST", json=json_body)


@app.put("/gateway/bookings/{booking_id}")
async def update_booking(booking_id: int, request: Request):
    json_body = await request.json()
    return await forward_request("booking", f"/bookings/{booking_id}", "PUT", json=json_body)


@app.delete("/gateway/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    return await forward_request("booking", f"/bookings/{booking_id}", "DELETE")


# ---------------- NOTIFICATION SERVICE ----------------

@app.get("/gateway/notifications")
async def get_all_notifications():
    return await forward_request("notification", "/notifications", "GET")


@app.get("/gateway/notifications/{notification_id}")
async def get_notification(notification_id: int):
    return await forward_request("notification", f"/notifications/{notification_id}", "GET")


@app.post("/gateway/notifications")
async def create_notification(request: Request):
    json_body = await request.json()
    return await forward_request("notification", "/notifications", "POST", json=json_body)


@app.put("/gateway/notifications/{notification_id}")
async def update_notification(notification_id: int, request: Request):
    json_body = await request.json()
    return await forward_request("notification", f"/notifications/{notification_id}", "PUT", json=json_body)


@app.delete("/gateway/notifications/{notification_id}")
async def delete_notification(notification_id: int):
    return await forward_request("notification", f"/notifications/{notification_id}", "DELETE")