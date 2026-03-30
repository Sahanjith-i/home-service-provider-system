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
    return {"message": "Service Provider Service is running"}