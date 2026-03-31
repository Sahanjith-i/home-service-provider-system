# API Gateway

The API Gateway serves as the central entry point for all microservices in the Home Service Provider system. It implements request routing, load balancing, and provides a unified API interface.

## Features

- **Request Routing**: Routes requests to appropriate microservices based on URL paths
- **CRUD Operations**: Full Create, Read, Update, Delete, and Patch operations for all services
- **Health Monitoring**: Health checks for gateway and all services
- **Error Handling**: Comprehensive error handling with standardized responses
- **CORS Support**: Cross-origin resource sharing enabled
- **Async/Await**: Non-blocking I/O for high performance

## Service Endpoints

### Booking Service (Port 8001)
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/{booking_id}` - Get booking by ID
- `PUT /api/bookings/{booking_id}` - Update booking
- `DELETE /api/bookings/{booking_id}` - Delete booking
- `PATCH /api/bookings/{booking_id}/status` - Update booking status

### Customer Service (Port 8002)
- `POST /api/customers/register` - Register customer
- `POST /api/customers/login` - Customer login
- `GET /api/customers` - Get all customers
- `GET /api/customers/{customer_id}` - Get customer by ID
- `PUT /api/customers/{customer_id}` - Update customer
- `PATCH /api/customers/{customer_id}` - Partial update customer
- `DELETE /api/customers/{customer_id}` - Delete customer

### Service Provider Service (Port 8003)
- `POST /api/providers` - Create service provider
- `GET /api/providers` - Get all service providers
- `GET /api/providers/{provider_id}` - Get provider by ID
- `PUT /api/providers/{provider_id}` - Update provider
- `PATCH /api/providers/{provider_id}/phone` - Update provider phone
- `DELETE /api/providers/{provider_id}` - Delete provider

### Notification Service (Port 8004)
- `POST /api/notifications` - Create notification
- `GET /api/notifications` - Get all notifications
- `GET /api/notifications/{notification_id}` - Get notification by ID
- `PUT /api/notifications/{notification_id}` - Update notification
- `DELETE /api/notifications/{notification_id}` - Delete notification
- `PATCH /api/notifications/{notification_id}/read` - Mark as read

## Health Endpoints

- `GET /` - Gateway status
- `GET /health` - Gateway health check
- `GET /health/services` - Health status of all services

## Configuration

Service URLs can be configured via environment variables:

- `BOOKING_SERVICE_URL` (default: http://localhost:8001)
- `CUSTOMER_SERVICE_URL` (default: http://localhost:8002)
- `SERVICE_PROVIDER_SERVICE_URL` (default: http://localhost:8003)
- `NOTIFICATION_SERVICE_URL` (default: http://localhost:8004)
- `API_GATEWAY_HOST` (default: 0.0.0.0)
- `API_GATEWAY_PORT` (default: 8000)

## Running the Gateway

```bash
cd api-gateway
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.</content>
<parameter name="filePath">d:\home-service-provider-system\api-gateway\README.md