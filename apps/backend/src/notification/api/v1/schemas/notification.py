"""
Pydantic schemas for Notification API.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.shared.api.schemas.base import ResponseSchema


class NotificationResponse(BaseModel):
    """Schema for a single notification in API responses."""

    id: str
    title: str
    message: str
    type: str = Field(validation_alias="notification_type")
    read: bool = Field(validation_alias="is_read")
    date: str = Field(validation_alias="created_at")
    notification_type: str

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    @field_validator("date", mode="before")
    @classmethod
    def convert_date_to_str(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d")
        if v is None:
            return datetime.now().strftime("%Y-%m-%d")
        return str(v)

    @field_validator("type", mode="before")
    @classmethod
    def map_type(cls, v):
        """Map the database notification_type to the frontend type field."""
        type_map = {
            "game_invite": "info",
            "course_enrollment": "success",
            "feedback_received": "info",
            "progress_update": "success",
            "achievement": "success",
            "system": "info",
            "reminder": "warning",
            "announcement": "info",
            "inactive_students": "warning",
            "unassigned_students": "warning",
            "new_registrations": "info",
            "weekly_summary": "info",
        }
        return type_map.get(v, "info")

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    """Response schema for listing notifications."""

    success: bool = True
    message: str = "Notificaciones obtenidas exitosamente"
    data: list[NotificationResponse]
    unread_count: int = 0
    total_count: int = 0


class NotificationReadResponse(ResponseSchema):
    """Response schema for mark-as-read operations."""

    data: dict | None = None


class NotificationDeleteResponse(ResponseSchema):
    """Response schema for delete operations."""

    data: dict | None = None
