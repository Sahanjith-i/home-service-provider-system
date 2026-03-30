import os
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .routes import router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Customer Service",
    description="Microservice for managing customer details, registration, and profiles",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": "Validation Error",
            "details": exc.errors(),
        },
    )


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "customer-service"}


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Service API",
        "version": "1.0.0",
        "endpoints": {
            "register": "POST /customers/register",
            "login": "POST /customers/login",
            "get_all": "GET /customers",
            "get_by_id": "GET /customers/{customer_id}",
            "update": "PUT /customers/{customer_id}",
            "delete": "DELETE /customers/{customer_id}",
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
