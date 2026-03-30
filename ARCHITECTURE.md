# API Gateway Architecture & Design Document

## Overview

The API Gateway is the single entry point for all microservices in the Home Service Provider system. It implements the **API Gateway pattern** - a common architectural pattern in microservices architectures.

## Architecture Pattern

```
Clients
   │
   ├─ Web Frontend
   ├─ Mobile App
   ├─ Third-party Integrations
   │
   └──► API Gateway (Central Proxy)
         │
         ├──► Service 1 (Provider Service)
         ├──► Service 2 (Booking Service)
         ├──► Service 3 (Customer Service)
         └──► Service 4 (Notification Service)
```

## Key Features

### 1. Request Routing
The gateway routes incoming requests to the appropriate microservice based on the URL path:

```python
/api/providers/*     ──► Service Provider Service (port 8003)
/api/bookings/*      ──► Booking Service (port 8001)
/api/customers/*     ──► Customer Service (port 8002)
/api/notifications/* ──► Notification Service (port 8004)
```

### 2. Service Proxy Function

The core of the gateway is the `proxy_request()` function:

```python
async def proxy_request(
    service_name: str,
    method: str,
    path: str,
    body: Optional[dict] = None,
    params: Optional[dict] = None
) -> dict:
    """
    Takes a request, forwards it to a microservice, 
    and returns the response
    """
```

**How it works:**
1. Receives request details
2. Constructs full service URL from environment config
3. Makes async HTTP request using httpx
4. Handles errors and HTTP status codes
5. Returns response to client

### 3. Async/Await Pattern

All functions use `async/await` for non-blocking I/O:

```python
@app.get("/api/providers")
async def get_all_providers():
    # Non-blocking call to service
    return await proxy_request("service-provider-service", "GET", "/providers")
```

**Benefits:**
- Thousands of concurrent connections
- Low memory footprint
- Fast response times

### 4. Health Monitoring

Three health check endpoints:

```
GET /              ─┐
GET /health        ├─► Gateway Health
GET /health/services ─► All Services Health
```

Example `/health/services` response:
```json
{
  "booking-service": {
    "status": "healthy",
    "url": "http://localhost:8001"
  },
  "customer-service": {
    "status": "healthy",
    "url": "http://localhost:8002"
  },
  "service-provider-service": {
    "status": "healthy",
    "url": "http://localhost:8003"
  },
  "notification-service": {
    "status": "healthy",
    "url": "http://localhost:8004"
  }
}
```

### 5. Error Handling

Handles multiple error scenarios:

```
Service Error
    │
    ├─ Connection Error (502 Bad Gateway)
    ├─ Timeout Error (502 Bad Gateway)
    ├─ HTTP 4xx Errors (Pass through)
    ├─ HTTP 5xx Errors (Pass through)
    └─ Unknown Service (404 Not Found)
```

All errors return standardized format:
```json
{
  "error": "HTTP Error | Internal Server Error",
  "status_code": 502,
  "detail": "Service 'booking-service' is unavailable"
}
```

### 6. CORS Support

Built-in CORS middleware allows requests from any origin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
```

**For production**, restrict origins:
```python
allow_origins=[
    "http://localhost:3000",
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

## Technical Implementation

### HTTP Client Lifecycle

The gateway uses httpx AsyncClient with proper lifecycle management:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    http_client = httpx.AsyncClient(timeout=30.0)
    
    yield  # App runs here
    
    # Shutdown
    await http_client.aclose()
```

**Benefits:**
- Connection pooling
- Automatic resource cleanup
- Better performance
- Proper error handling

### Logging System

Comprehensive logging throughout:

```python
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Log messages include:**
- Service startup/shutdown
- Request routing information
- Service response status codes
- Error details and stack traces

### Environment Configuration

Service URLs loaded from environment variables:

```python
SERVICE_URLS = {
    "booking-service": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8001"),
    "customer-service": os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8002"),
    "service-provider-service": os.getenv("SERVICE_PROVIDER_SERVICE_URL", "http://localhost:8003"),
    "notification-service": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004"),
}
```

**Advantages:**
- Easy to configure for different environments
- No hardcoded values
- Supports DNS names or IP addresses
- Can point to remote services

## Request Flow Example

### Creating a Service Provider

```
1. Client Request
   POST /api/providers
   {
     "name": "John Plumber",
     "service_type": "Plumber",
     ...
   }
   │
   ├─► API Gateway receives request
   │
   ├─► Routes to create_provider() function
   │
   ├─► Calls proxy_request(
   │       "service-provider-service",
   │       "POST",
   │       "/providers",
   │       body=provider_data
   │   )
   │
   ├─► proxy_request() constructs URL:
   │   "http://localhost:8003/providers"
   │
   ├─► Makes HTTP POST request via httpx
   │
   ├─► Receives response from Service Provider Service
   │
   └─► Returns response to client

2. Response
   {
     "message": "Service provider created successfully",
     "provider": {
       "provider_id": 1,
       "name": "John Plumber",
       ...
     }
   }
```

## Configuration Management

### Environment File Structure

```env
# Gateway Configuration
API_GATEWAY_HOST=0.0.0.0
API_GATEWAY_PORT=8000
DEBUG=True

# Service URLs
BOOKING_SERVICE_URL=http://localhost:8001
CUSTOMER_SERVICE_URL=http://localhost:8002
SERVICE_PROVIDER_SERVICE_URL=http://localhost:8003
NOTIFICATION_SERVICE_URL=http://localhost:8004
```

### Runtime Configuration

```python
if __name__ == "__main__":
    host = os.getenv("API_GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("API_GATEWAY_PORT", 8000))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
```

## Adding New Routes

### Step 1: Identify the Service
Determine which microservice handles this resource:
- Service Providers → service-provider-service
- Bookings → booking-service
- Customers → customer-service
- Notifications → notification-service

### Step 2: Add Gateway Route

```python
@app.post("/api/resource", tags=["Resources"])
async def create_resource(resource_data: dict):
    """Create a new resource"""
    return await proxy_request("target-service", "POST", "/resource", body=resource_data)
```

### Step 3: Add Microservice Route

In `target-service/app/routes.py`:
```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/resource")
def create_resource(resource: ResourceCreate):
    # Implementation here
    pass
```

### Step 4: Include Router in Microservice

In `target-service/app/main.py`:
```python
from app.routes import router
app.include_router(router)
```

## Performance Considerations

### Connection Pooling

By default, httpx uses connection pooling:
- Maintains persistent connections
- Reduces connection overhead
- Handles keep-alive automatically

### Timeout Configuration

```python
http_client = httpx.AsyncClient(timeout=30.0)
```

- 30 second timeout for all service calls
- Prevents hanging requests
- Configurable per need

### Concurrent Requests

Uvicorn handles concurrent requests:
```bash
# Start with multiple workers
uvicorn app.main:app --workers 4
```

## Security Considerations

### Current Setup
- ✅ CORS configured for development
- ✅ Proper error messages (no stack traces to client)
- ✅ Async prevents blocking attacks
- ❌ No authentication/authorization
- ❌ No rate limiting
- ❌ No request validation

### Production Hardening

```python
# 1. Add Authentication
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/providers")
async def create_provider(
    provider_data: dict,
    credentials = Depends(security)
):
    # Verify JWT token
    pass

# 2. Add Rate Limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/providers")
@limiter.limit("100/minute")
async def get_all_providers(request: Request):
    pass

# 3. Input Validation
from pydantic import BaseModel

class ProviderCreate(BaseModel):
    name: str
    service_type: str
    # ... other fields with validation

@app.post("/api/providers")
async def create_provider(provider: ProviderCreate):
    return await proxy_request(...)

# 4. CORS Restriction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Monitoring & Observability

### Metrics to Track

1. **Request Count**: Total requests per service
2. **Response Time**: Latency to each service
3. **Error Rate**: Percentage of failed requests
4. **Service Availability**: Uptime per service
5. **Gateway Health**: CPU, memory usage

### Implementation Options

```python
# Option 1: Prometheus + Grafana
from prometheus_client import Counter, Histogram

request_count = Counter('gateway_requests_total', 'Total requests', ['service'])
request_duration = Histogram('gateway_request_duration_seconds', 'Request duration', ['service'])

# Option 2: Distributed Tracing
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

# Option 3: Application Performance Monitoring (APM)
# Use services like DataDog, New Relic, or Elastic
```

## Scaling Strategy

### Horizontal Scaling

```
Load Balancer (nginx, HAProxy)
    │
    ├─► API Gateway Instance 1
    ├─► API Gateway Instance 2
    └─► API Gateway Instance 3
         │
         └─► Microservices (shared backend)
```

### Database Scaling

```
Microservices
    │
    ├─► MongoDB Primary (writes)
    └─► MongoDB Secondaries (reads)
```

## Testing

### Unit Tests

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_proxy_request():
    response = client.get("/api/providers")
    assert response.status_code == 200
```

### Integration Tests

```python
# Test actual service communication
def test_create_provider_end_to_end():
    provider_data = {
        "name": "Test Provider",
        "service_type": "Plumber",
        # ... other fields
    }
    response = client.post("/api/providers", json=provider_data)
    assert response.status_code in [200, 201]
```

## Troubleshooting Guide

### Issue: 502 Bad Gateway

**Causes:**
- Service not running
- Wrong service URL
- Service crashed

**Debug steps:**
```bash
# Check service health
curl http://localhost:8000/health/services

# Check service directly
curl http://localhost:8003/

# Check service URL in gateway
cat api-gateway/.env | grep SERVICE_URL
```

### Issue: Timeout

**Causes:**
- Service slow/hanging
- Network connectivity
- Resource limits

**Debug steps:**
```bash
# Increase timeout
# In api-gateway/app/main.py:
# http_client = httpx.AsyncClient(timeout=60.0)

# Check service logs
tail -f service-provider-service.log
```

### Issue: High Latency

**Causes:**
- Service slow
- Network latency
- Connection pool exhausted

**Debug steps:**
```bash
# Monitor gateway metrics
curl http://localhost:8000/metrics

# Check service performance
python -m cProfile -s cumulative service_provider_service/app/main.py
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [httpx Documentation](https://www.python-httpx.org/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Microservices Patterns](https://microservices.io/patterns/apigateway.html)

