# Microservices Deployment Guide

## Prerequisites

- Python 3.10+
- MongoDB (local or cloud instance)
- Git/Version Control
- Terminal/Command Line

## Step-by-Step Deployment

### Phase 1: Environment Setup

#### 1.1 Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 1.2 Install Common Dependencies

```bash
pip install -r requirements-common.txt
```

#### 1.3 Verify Common Dependencies

```bash
python -c "import fastapi; import uvicorn; import httpx; print('✅ All common packages installed')"
```

### Phase 2: Service Configuration

#### 2.1 Create Environment Files

For each service, create a `.env` file from `.env.template`:

```bash
# API Gateway
cd api-gateway
copy .env.template .env  # Windows
# or
cp .env.template .env   # macOS/Linux

# Repeat for each service:
# - booking-service
# - customer-service
# - service-provider-service
# - notification-service
```

#### 2.2 Update Service URLs (if running on different machines)

In `api-gateway/.env`:
```env
BOOKING_SERVICE_URL=http://your-booking-server:8001
CUSTOMER_SERVICE_URL=http://your-customer-server:8002
SERVICE_PROVIDER_SERVICE_URL=http://your-provider-server:8003
NOTIFICATION_SERVICE_URL=http://your-notification-server:8004
```

### Phase 3: MongoDB Configuration (If Using Databases)

#### 3.1 Install MongoDB

- **Local**: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
- **Cloud**: Use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

#### 3.2 Update MongoDB Connection Strings

In each service's `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
# OR for Atlas:
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

#### 3.3 Initialize Database Collections (Optional)

```bash
python -c "
from service_provider_service.app.database import provider_collection
print(f'✅ Connected to {provider_collection.database.name}')
"
```

### Phase 4: Start Services

#### 4.1 Option 1: Start All in One Terminal (Sequential)

```bash
# This will start services one by one - only one will run at a time
bash start_services.sh  # (if you create this helper script)
```

#### 4.2 Option 2: Start Each Service Individually

**Terminal 1 - API Gateway**
```bash
cd api-gateway
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Service Provider Service**
```bash
cd service-provider-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

**Terminal 3 - Booking Service**
```bash
cd booking-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 4 - Customer Service**
```bash
cd customer-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 5 - Notification Service**
```bash
cd notification-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

#### 4.3 Option 3: Use Docker (Advanced)

Create `docker-compose.yml`:

```yaml
version: '3'
services:
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_DATABASE: home_service

  api-gateway:
    build: ./api-gateway
    ports:
      - "8000:8000"
    depends_on:
      - mongo
    environment:
      BOOKING_SERVICE_URL: http://booking-service:8001
      CUSTOMER_SERVICE_URL: http://customer-service:8002
      SERVICE_PROVIDER_SERVICE_URL: http://service-provider-service:8003
      NOTIFICATION_SERVICE_URL: http://notification-service:8004

  booking-service:
    build: ./booking-service
    ports:
      - "8001:8001"
    depends_on:
      - mongo

  customer-service:
    build: ./customer-service
    ports:
      - "8002:8002"
    depends_on:
      - mongo

  service-provider-service:
    build: ./service-provider-service
    ports:
      - "8003:8003"
    depends_on:
      - mongo

  notification-service:
    build: ./notification-service
    ports:
      - "8004:8004"
    depends_on:
      - mongo
```

Then run:
```bash
docker-compose up -d
```

### Phase 5: Verification

#### 5.1 Check API Gateway Status

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "running",
  "application": "Home Service Provider API Gateway",
  "version": "1.0.0"
}
```

#### 5.2 Check All Services Health

```bash
curl http://localhost:8000/health/services
```

#### 5.3 Access API Documentation

Open in browser:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

#### 5.4 Test an Endpoint

```bash
curl -X GET http://localhost:8000/api/providers \
  -H "Content-Type: application/json"
```

### Phase 6: Monitoring & Logs

#### 6.1 Monitor Service Health

```bash
# Create a monitoring script
watch -n 5 'curl -s http://localhost:8000/health/services | python -m json.tool'
```

#### 6.2 View Service Logs

Each terminal running a service shows real-time logs. Look for:
- ✅ "successfully" messages (good)
- ❌ "error" messages (check configuration)
- 🔴 "connection refused" (service not running)

#### 6.3 Common Log Patterns

```
2024-03-30 10:00:00 - root - INFO - API Gateway started - HTTP client initialized
✅ Indicates successful startup

2024-03-30 10:00:05 - root - ERROR - Service 'booking-service' error: Connection refused
❌ Indicates service is not running on expected port
```

## Troubleshooting Deployment Issues

### Issue: "Connection refused" on port 8000

**Solution:**
```bash
# Check if port is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process using the port
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: "Service unavailable" when calling API Gateway

**Solution:**
1. Verify all services are running
2. Check `/health/services` endpoint
3. Verify service URLs in `api-gateway/.env`
4. Check firewall/network settings

### Issue: MongoDB connection error

**Solution:**
```bash
# Test MongoDB connection
mongosh "mongodb://localhost:27017"

# If MongoDB isn't running, start it
# Windows: mongod.exe
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### Issue: Port already in use

**Solution:**
```bash
# Change port in .env file, e.g.:
BOOKING_SERVICE_PORT=8011  # instead of 8001

# Update in api-gateway/.env:
BOOKING_SERVICE_URL=http://localhost:8011
```

## Production Deployment Checklist

- [ ] All `.env` files configured (no defaults used)
- [ ] MongoDB credentials secured
- [ ] CORS settings appropriate for domain
- [ ] Logging configured for production
- [ ] Health checks responding
- [ ] Load testing completed
- [ ] API documentation reviewed
- [ ] Error handling tested
- [ ] Rate limiting configured (if needed)
- [ ] API keys/authentication configured
- [ ] SSL/TLS certificates installed
- [ ] Monitoring/alerting set up
- [ ] Database backups configured
- [ ] Deployment documentation updated

## Scaling Considerations

### Horizontal Scaling

```yaml
# docker-compose.yml for scaling
version: '3'
services:
  booking-service:
    image: booking-service
    deploy:
      replicas: 3
    ports:
      - "8001-8003:8001"
```

### Load Balancing

Use Nginx or similar:
```nginx
upstream booking_service {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

### Caching

Consider adding Redis for caching:
```yaml
services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

## Performance Tuning

1. **Connection Pooling**: Increase in `main.py`:
   ```python
   http_client = httpx.AsyncClient(limits=httpx.Limits(max_connections=100))
   ```

2. **Uvicorn Workers**: Start with multiple workers
   ```bash
   uvicorn app.main:app --workers 4
   ```

3. **MongoDB Indexes**: Create indexes for frequently queried fields

## Maintenance

### Regular Tasks

- Monitor logs for errors
- Update dependencies monthly
- Back up MongoDB weekly
- Review API usage metrics
- Test disaster recovery procedures

### Updating Services

```bash
# Update code
git pull

# Restart services
ctrl+c  # Stop running service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

