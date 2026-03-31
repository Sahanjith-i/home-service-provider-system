from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Service Provider Service",
    version="1.0.0",
    description="CRUD API for managing service providers"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Service Provider Service",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "service-provider-service"
    }