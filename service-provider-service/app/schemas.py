from pydantic import BaseModel, EmailStr
from typing import Optional


class ServiceProviderCreate(BaseModel):
    name: str
    service_type: str
    phone: str
    email: EmailStr
    location: str
    availability_status: str = "available"


class ServiceProviderUpdate(BaseModel):
    name: Optional[str] = None
    service_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    availability_status: Optional[str] = None