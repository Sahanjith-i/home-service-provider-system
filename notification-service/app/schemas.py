from pydantic import BaseModel, Field, field_validator, root_validator
from datetime import datetime

VALID_TYPES = ["booking", "payment", "system", "payment_confirmation"]


class NotificationCreate(BaseModel):
    user_id: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)
    notification_type: str | None = None
    type: str | None = None
    created_at: datetime
    is_read: bool = False

    @root_validator(pre=True)
    def normalize_type_field(cls, values):
        # support both `type` and `notification_type` in incoming payload
        if values.get("type") and not values.get("notification_type"):
            values["notification_type"] = values["type"]
        return values

    @field_validator("notification_type")
    @classmethod
    def validate_type(cls, v):
        if v not in VALID_TYPES:
            raise ValueError("Invalid notification type")
        return v