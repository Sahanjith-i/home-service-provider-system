# Quick Start Guide - Running the Home Service Provider System

## 30-Second Setup

### 1. Install Dependencies
```bash
pip install -r requirements-common.txt
```

### 2. Start API Gateway
```bash
cd api-gateway
python -m uvicorn app.main:app --port 8000 --reload
```

### 3. Start Service Provider Service
```bash
cd service-provider-service
python -m uvicorn app.main:app --port 8003 --reload
```

### 4. Start Other Services (in separate terminals)
```bash
# Booking Service
cd booking-service
python -m uvicorn app.main:app --port 8001 --reload

# Customer Service
cd customer-service
python -m uvicorn app.main:app --port 8002 --reload

# Notification Service
cd notification-service
python -m uvicorn app.main:app --port 8004 --reload
```

## Test It Out

### Check If Everything Works
```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "status": "running",
  "application": "Home Service Provider API Gateway",
  "version": "1.0.0"
}
```

### Check Service Health
```bash
curl http://localhost:8000/health/services
```

### View Interactive API Documentation
Open in browser: **http://localhost:8000/docs**

## Using the API

### Create a Service Provider
```bash
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
```

### Get All Providers
```bash
curl http://localhost:8000/api/providers
```

### Get Specific Provider
```bash
curl http://localhost:8000/api/providers/1
```

## Common Ports

- **API Gateway**: http://localhost:8000
- **Booking Service**: http://localhost:8001
- **Customer Service**: http://localhost:8002
- **Service Provider Service**: http://localhost:8003
- **Notification Service**: http://localhost:8004

## API Documentation

Each service has Swagger documentation:
- API Gateway: http://localhost:8000/docs
- Booking Service: http://localhost:8001/docs
- Customer Service: http://localhost:8002/docs
- Service Provider Service: http://localhost:8003/docs
- Notification Service: http://localhost:8004/docs

## Stopping Services

Press `Ctrl+C` in each terminal to stop the services.

## Configuration

- API Gateway service URLs: `api-gateway/.env`
- Individual service settings: `{service-name}/.env`
- Create `.env` files from `.env.template` files if needed

## Troubleshooting

### Module import errors
```bash
pip install -r requirements-common.txt
cd {service-directory}
pip install -r requirements.txt
```

### Port already in use
```bash
# Edit .env file and change port, e.g.:
API_GATEWAY_PORT=8005
```

### Service unavailable error
- Make sure all services are running
- Check `/health/services` endpoint
- Verify service URLs in `api-gateway/.env`

## Next: Full Setup & Deployment

See **SETUP.md** for detailed configuration and **DEPLOYMENT.md** for production deployment.
