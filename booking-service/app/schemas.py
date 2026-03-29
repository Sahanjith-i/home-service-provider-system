from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

VALID_SERVICE_TYPES = [
    "plumbing",
    "cleaning",
    "electrician",
    "painting",
    "gardening",
    "pest_control",
    "carpentry",
    "air_conditioning"
]

VALID_STATUS = ["pending", "confirmed", "completed", "cancelled"]


class BookingCreate(BaseModel):
    customer_id: str = Field(..., min_length=2)
    provider_id: str = Field(..., min_length=2)
    service_type: str
    booking_date: datetime
    address: str = Field(..., min_length=5)

    @validator("service_type")
    def validate_service_type(cls, v):
        if v not in VALID_SERVICE_TYPES:
            raise ValueError("Invalid service type")
        return v


class BookingUpdate(BaseModel):
    customer_id: Optional[str]
    provider_id: Optional[str]
    service_type: Optional[str]
    booking_date: Optional[datetime]
    address: Optional[str]
    status: Optional[str]

    @validator("service_type")
    def validate_service_type(cls, v):
        if v and v not in VALID_SERVICE_TYPES:
            raise ValueError("Invalid service type")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v and v not in VALID_STATUS:
            raise ValueError("Invalid status")
        return v