# Backend Details

This project uses a microservice backend behind a FastAPI API gateway.

## Services

### API Gateway
- Path: `api-gateway/app/main.py`
- Port: `8000`
- Purpose: single entry point that proxies requests to backend services
- Health endpoints:
  - `GET /`
  - `GET /health`
  - `GET /health/services`

### Customer Service
- Path: `customer-service/app/main.py`
- Port: `8001`
- Files:
  - `customer-service/app/database.py`
  - `customer-service/app/models.py`
  - `customer-service/app/routes.py`
  - `customer-service/app/schemas.py`
- Core schemas:
  - `RegisterRequest`
  - `RegisterResponse`
  - `LoginRequest`
  - `LoginResponse`
  - `UpdateProfileRequest`
  - `CustomerDetailResponse`
  - `AllCustomersResponse`
- Main routes:
  - `POST /customers/register`
  - `POST /customers/login`
  - `GET /customers`
  - `GET /customers/{customer_id}`
  - `PUT /customers/{customer_id}`
  - `PATCH /customers/{customer_id}`
  - `DELETE /customers/{customer_id}`

### Service Provider Service
- Path: `service-provider-service/app/main.py`
- Port: `8002`
- Files:
  - `service-provider-service/app/database.py`
  - `service-provider-service/app/models.py`
  - `service-provider-service/app/routes.py`
  - `service-provider-service/app/schemas.py`
- Core schemas:
  - `ServiceProviderCreate`
  - `ServiceProviderUpdate`
  - `ProviderPhoneUpdate`
  - `ServiceProviderResponse`
  - `ServiceProviderMutationResponse`
- Main routes:
  - `GET /`
  - `GET /health`
  - `POST /providers`
  - `GET /providers`
  - `GET /providers/{provider_id}`
  - `PUT /providers/{provider_id}`
  - `PATCH /providers/{provider_id}/phone`
  - `DELETE /providers/{provider_id}`

### Booking Service
- Path: `booking-service/app/main.py`
- Port: `8003`
- Files:
  - `booking-service/app/database.py`
  - `booking-service/app/models.py`
  - `booking-service/app/routes.py`
  - `booking-service/app/schemas.py`
- Core schemas:
  - `BookingCreate`
  - `BookingUpdate`
  - `BookingResponse`
- Main routes:
  - `GET /`
  - `GET /health`
  - `POST /bookings`
  - `GET /bookings`
  - `GET /bookings/{booking_id}`
  - `PUT /bookings/{booking_id}`
  - `PATCH /bookings/{booking_id}/status`
  - `DELETE /bookings/{booking_id}`

### Notification Service
- Path: `notification-service/app/main.py`
- Port: `8004`
- Files:
  - `notification-service/app/database.py`
  - `notification-service/app/models.py`
  - `notification-service/app/routes.py`
  - `notification-service/app/schemas.py`
- Core schemas:
  - `NotificationCreate`
  - `NotificationResponse`
- Main routes:
  - `GET /`
  - `GET /health`
  - `POST /api/notifications`
  - `GET /api/notifications`
  - `GET /api/notifications/{notification_id}`
  - `PUT /api/notifications/{notification_id}`
  - `PATCH /api/notifications/{notification_id}/read`
  - `DELETE /api/notifications/{notification_id}`

## Notes

- Request and response schemas are now attached to routes, so FastAPI docs expose the full backend structure.
- OpenAPI docs are available on each running FastAPI service at `/docs`.
- Gateway docs are available at `http://127.0.0.1:8000/docs` when the gateway is running.