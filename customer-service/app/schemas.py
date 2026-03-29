from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class CustomerSchema(BaseModel):
    """Customer schema for database operations"""
    customer_id: str
    name: str
    email: EmailStr
    phone: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    password_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema"""
    success: bool
    message: str
    customer: Optional[dict] = None
    token: Optional[str] = None


class RegisterRequest(BaseModel):
    """Register request schema"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=500)
    password: str = Field(..., min_length=8)
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class RegisterResponse(BaseModel):
    """Register response schema"""
    success: bool
    message: str
    customer_id: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    """Update profile request schema"""
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerDetailResponse(BaseModel):
    """Customer detail response schema"""
    customer_id: str
    name: str
    email: str
    phone: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    created_at: str
    updated_at: str


class AllCustomersResponse(BaseModel):
    """All customers response schema"""
    total: int
    customers: List[CustomerDetailResponse]
