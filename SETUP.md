# Home Service Provider System - Setup & Architecture Guide

## System Overview

This is a **microservices-based home service provider platform** built with FastAPI and MongoDB. The system consists of:

1. **API Gateway** (Port 8000) - Main entry point
2. **Service Provider Service** (Port 8003) - Manages service providers
3. **Booking Service** (Port 8001) - Manages bookings
4. **Customer Service** (Port 8002) - Manages customers
5. **Notification Service** (Port 8004) - Handles notifications

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   API GATEWAY    │ (Port 8000)
                    │   (Main Router)  │
                    └────────┬─────────┘
                             │
                ┌────────────┼────────────┬────────────┐
                ▼            ▼            ▼            ▼
          ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
          │Booking   │  │Customer  │  │Service   │  │Notification │
          │Service   │  │Service   │  │Provider  │  │Service       │
          │(8001)    │  │(8002)    │  │Service   │  │(8004)        │
          │          │  │          │  │(8003)    │  │              │
          └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
               │             │             │               │
               └─────────────┴─────────────┴───────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   MongoDB        │
                    │  (shared or per  │
                    │  service DBs)    │
                    └──────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
# Install common dependencies
pip install -r requirements-common.txt

# Install API Gateway dependencies
cd api-gateway
pip install -r requirements.txt

# Install each microservice dependencies
cd ../booking-service
pip install -r requirements.txt

cd ../customer-service
pip install -r requirements.txt

cd ../service-provider-service
pip install -r requirements.txt

cd ../notification-service
pip install -r requirements.txt
```

### 2. Environment Setup

Each service has a `.env.template` file. Create `.env` files by copying:

```bash
# API Gateway
copy api-gateway\.env.template api-gateway\.env

# Booking Service
copy booking-service\.env.template booking-service\.env

# Customer Service
copy customer-service\.env.template customer-service\.env

# Service Provider Service
copy service-provider-service\.env.template service-provider-service\.env

# Notification Service
copy notification-service\.env.template notification-service\.env
```

### 3. Start Services

**Option A: Start services individually in different terminals**

```bash
# Terminal 1 - API Gateway
cd api-gateway
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Service Provider Service
cd service-provider-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# Terminal 3 - Booking Service
cd booking-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 4 - Customer Service
cd customer-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 5 - Notification Service
cd notification-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

**Option B: Use the provided run scripts (if available)**

## API Gateway Features

The API Gateway provides:

### Health Check Endpoints
- `GET /` - Gateway status
- `GET /health` - Gateway health
- `GET /health/services` - All microservices health status

### Service Provider Routes
```
POST   /api/providers                  - Create provider
GET    /api/providers                  - Get all providers
GET    /api/providers/{provider_id}    - Get provider by ID
PUT    /api/providers/{provider_id}    - Update provider
PATCH  /api/providers/{provider_id}/phone - Update phone
DELETE /api/providers/{provider_id}    - Delete provider
```

### Booking Routes
```
POST   /api/bookings                   - Create booking
GET    /api/bookings                   - Get all bookings
GET    /api/bookings/{booking_id}      - Get booking by ID
PUT    /api/bookings/{booking_id}      - Update booking
PATCH  /api/bookings/{booking_id}/status - Update status
DELETE /api/bookings/{booking_id}      - Delete booking
```

### Customer Routes
```
POST   /api/customers                  - Create customer
GET    /api/customers                  - Get all customers
GET    /api/customers/{customer_id}    - Get customer by ID
PUT    /api/customers/{customer_id}    - Update customer
DELETE /api/customers/{customer_id}    - Delete customer
```

### Notification Routes
```
POST   /api/notifications              - Send notification
GET    /api/notifications              - Get all notifications
GET    /api/notifications/{notification_id} - Get by ID
DELETE /api/notifications/{notification_id} - Delete
```

## API Gateway Configuration

The API Gateway automatically:
- Routes all requests to appropriate microservices
- Handles connection failures with proper error messages
- Provides CORS support
- Implements async/await for high performance
- Includes comprehensive logging
- Provides service health monitoring

### Service URLs Configuration

Edit `api-gateway/.env`:
```env
BOOKING_SERVICE_URL=http://localhost:8001
CUSTOMER_SERVICE_URL=http://localhost:8002
SERVICE_PROVIDER_SERVICE_URL=http://localhost:8003
NOTIFICATION_SERVICE_URL=http://localhost:8004
```

## Example Usage

### Using curl

```bash
# Check API Gateway status
curl http://localhost:8000/

# Check all services health
curl http://localhost:8000/health/services

# Create a service provider
curl -X POST http://localhost:8000/api/providers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Plumber",
    "service_type": "Plumber",
    "phone": "0123456789",
    "email": "john@example.com",
    "location": "New York",
    "availability_status": "available"
  }'

# Get all providers
curl http://localhost:8000/api/providers

# Get specific provider
curl http://localhost:8000/api/providers/1
```

### Using Python requests

```python
import requests

base_url = "http://localhost:8000"

# Check health
response = requests.get(f"{base_url}/health")
print(response.json())

# Create provider
provider_data = {
    "name": "Jane Electrician",
    "service_type": "Electrician",
    "phone": "0987654321",
    "email": "jane@example.com",
    "location": "Los Angeles",
    "availability_status": "available"
}
response = requests.post(f"{base_url}/api/providers", json=provider_data)
print(response.json())
```

## API Documentation

Once running, access the interactive Swagger documentation:
- **API Gateway**: http://localhost:8000/docs
- **Service Provider Service**: http://localhost:8003/docs
- **Booking Service**: http://localhost:8001/docs
- **Customer Service**: http://localhost:8002/docs
- **Notification Service**: http://localhost:8004/docs

## Direct Service Access

You can also access services directly bypassing the gateway:

```bash
# Direct access to Service Provider Service
curl http://localhost:8003/providers

# Direct access to Booking Service
curl http://localhost:8001/bookings
```

## Development Notes

### Adding New Endpoints

1. **In a microservice** (e.g., booking-service):
   - Add route in `app/routes.py`
   - Add schema in `app/schemas.py`
   - Update `app/main.py` to include routes

2. **In API Gateway**:
   - Add new proxy route in `api-gateway/app/main.py`
   - Use the `proxy_request()` function for consistency

### Error Handling

The API Gateway handles:
- Service unavailability (502 Bad Gateway)
- Connection timeouts
- Invalid requests (4xx errors)
- Server errors (5xx errors)

## Common Issues & Troubleshooting

### "Service unavailable" error
- Ensure all microservices are running
- Check service URLs in `api-gateway/.env`
- Verify ports are not being used by other applications

### "Connection refused"
- Check MongoDB connection if services require it
- Ensure `MONGODB_URL` is correctly configured in `.env`

### CORS errors
- The gateway includes CORS middleware - should work for most clients
- Adjust CORS settings if needed in `api-gateway/app/main.py`

## Project Structure

```
home-service-provider-system/
├── api-gateway/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py  ← API Gateway entry point
│   ├── .env  ← Create from .env.template
│   └── requirements.txt
├── booking-service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py  ← Service entry point
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   └── database.py
│   ├── .env  ← Create from .env.template
│   └── requirements.txt
├── customer-service/  [Similar structure]
├── service-provider-service/  [Similar structure]
├── notification-service/  [Similar structure]
├── requirements-common.txt
└── README.md
```

## Next Steps

1. **Configure MongoDB** - Update `.env` files with MongoDB connection strings
2. **Implement Routes** - Fill in route handlers in each service's `routes.py`
3. **Add Schemas** - Define request/response schemas in `schemas.py`
4. **Implement Database** - Set up MongoDB connections in `database.py`
5. **Add Tests** - Create test files for each service

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Python Driver](https://docs.mongodb.com/drivers/pymongo/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

