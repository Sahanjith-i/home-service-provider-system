from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Customer Service",
    version="1.0.0",
    description="CRUD API for managing customers"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Customer Service is running"}