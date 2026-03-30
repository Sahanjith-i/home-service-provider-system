from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    """Base customer model with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=500)
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerRegister(CustomerBase):
    """Customer registration model"""
    password: str = Field(..., min_length=8)


class CustomerLogin(BaseModel):
    """Customer login model"""
    email: EmailStr
    password: str


class CustomerUpdate(BaseModel):
    """Customer update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, min_length=5, max_length=500)
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerProfileUpdate(BaseModel):
    """Customer profile update model"""
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerResponse(BaseModel):
    """Customer response model"""
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

    class Config:
        from_attributes = True


class CustomerInDB(CustomerBase):
    """Customer database model"""
    customer_id: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
