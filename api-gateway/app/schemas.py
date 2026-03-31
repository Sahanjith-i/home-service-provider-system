from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ServiceProviderCreateRequest(BaseModel):
    name: str
    service_type: str
    phone: str
    email: EmailStr
    location: str
    availability_status: str = "available"


class ServiceProviderUpdateRequest(BaseModel):
    name: Optional[str] = None
    service_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    availability_status: Optional[str] = None


class BookingCreateRequest(BaseModel):
    customer_id: str = Field(..., min_length=2)
    provider_id: str = Field(..., min_length=2)
    service_type: str
    booking_date: datetime
    address: str = Field(..., min_length=5)


class BookingUpdateRequest(BaseModel):
    customer_id: Optional[str] = None
    provider_id: Optional[str] = None
    service_type: Optional[str] = None
    booking_date: Optional[datetime] = None
    address: Optional[str] = None
    status: Optional[str] = None


class RegisterCustomerRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=500)
    password: str = Field(..., min_length=8)
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class LoginCustomerRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateCustomerRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class NotificationRequest(BaseModel):
    user_id: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)
    notification_type: Optional[str] = None
    type: Optional[str] = None
    created_at: datetime
    is_read: bool = False