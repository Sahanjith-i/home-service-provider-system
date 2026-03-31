from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class ServiceProviderCreate(BaseModel):
    name: str
    service_type: str
    phone: str
    email: EmailStr
    location: str
    availability_status: str = "available"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value.strip()

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, value: str):
        allowed_types = ["Plumber", "Electrician", "Cleaner", "Painter", "Carpenter"]
        if not value.strip():
            raise ValueError("Service type cannot be empty")
        if value.strip() not in allowed_types:
            raise ValueError(
                f"Service type must be one of: {', '.join(allowed_types)}"
            )
        return value.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        phone = value.strip()
        if not phone.isdigit():
            raise ValueError("Phone number must contain digits only")
        if len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        if not phone.startswith("0"):
            raise ValueError("Phone number must start with 0")
        return phone

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr):
        email = str(value).strip()
        if "@" not in email:
            raise ValueError("Email must contain '@' symbol")
        if "." not in email.split("@")[-1]:
            raise ValueError("Email must contain a domain (e.g., gmail.com)")
        return email

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str):
        if not value.strip():
            raise ValueError("Location cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Location must be at least 3 characters long")
        return value.strip()

    @field_validator("availability_status")
    @classmethod
    def validate_availability_status(cls, value: str):
        allowed_status = ["available", "unavailable", "busy"]
        if value.strip().lower() not in allowed_status:
            raise ValueError(
                f"Availability status must be one of: {', '.join(allowed_status)}"
            )
        return value.strip().lower()


class ServiceProviderUpdate(BaseModel):
    name: Optional[str] = None
    service_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    availability_status: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]):
        if value is not None:
            if not value.strip():
                raise ValueError("Name cannot be empty")
            if len(value.strip()) < 3:
                raise ValueError("Name must be at least 3 characters long")
            return value.strip()
        return value

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, value: Optional[str]):
        allowed_types = ["Plumber", "Electrician", "Cleaner", "Painter", "Carpenter"]
        if value is not None:
            if not value.strip():
                raise ValueError("Service type cannot be empty")
            if value.strip() not in allowed_types:
                raise ValueError(
                    f"Service type must be one of: {', '.join(allowed_types)}"
                )
            return value.strip()
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]):
        if value is not None:
            phone = value.strip()
            if not phone.isdigit():
                raise ValueError("Phone number must contain digits only")
            if len(phone) != 10:
                raise ValueError("Phone number must be exactly 10 digits")
            if not phone.startswith("0"):
                raise ValueError("Phone number must start with 0")
            return phone
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[EmailStr]):
        if value is not None:
            email = str(value).strip()
            if "@" not in email:
                raise ValueError("Email must contain '@' symbol")
            if "." not in email.split("@")[-1]:
                raise ValueError("Email must contain a valid domain")
            return email
        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: Optional[str]):
        if value is not None:
            if not value.strip():
                raise ValueError("Location cannot be empty")
            if len(value.strip()) < 3:
                raise ValueError("Location must be at least 3 characters long")
            return value.strip()
        return value

    @field_validator("availability_status")
    @classmethod
    def validate_availability_status(cls, value: Optional[str]):
        allowed_status = ["available", "unavailable", "busy"]
        if value is not None:
            if value.strip().lower() not in allowed_status:
                raise ValueError(
                    f"Availability status must be one of: {', '.join(allowed_status)}"
                )
            return value.strip().lower()
        return value


# PATCH schema (for phone update)
class ProviderPhoneUpdate(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        phone = value.strip()
        if not phone.isdigit():
            raise ValueError("Phone number must contain digits only")
        if len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        if not phone.startswith("0"):
            raise ValueError("Phone number must start with 0")
        return phone


class ServiceProviderResponse(BaseModel):
    provider_id: Optional[int] = None
    name: str
    service_type: str
    phone: str
    email: EmailStr
    location: str
    availability_status: str


class ServiceProviderMutationResponse(BaseModel):
    message: str
    provider: ServiceProviderResponse


class MessageResponse(BaseModel):
    message: str