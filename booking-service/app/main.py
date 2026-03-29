from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Booking Service", version="2.0.0")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "🚀 Booking Service with Auto Increment is running"}