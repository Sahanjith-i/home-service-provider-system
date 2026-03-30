from pydantic import BaseModel, Field, field_validator
from datetime import datetime

VALID_TYPES = ["booking", "payment", "system"]


class NotificationCreate(BaseModel):
    user_id: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)
    notification_type: str
    created_at: datetime
    is_read: bool = False

    @field_validator("notification_type")
    @classmethod
    def validate_type(cls, v):
        if v not in VALID_TYPES:
            raise ValueError("Invalid notification type")
        return v