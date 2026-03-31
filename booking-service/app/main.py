from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Booking Service",
    version="1.0.0",
    description="CRUD API for managing bookings"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Booking Service is running"}