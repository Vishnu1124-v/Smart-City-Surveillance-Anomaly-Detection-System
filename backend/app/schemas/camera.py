from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CameraCreate(BaseModel):
    name: str
    location: Optional[str] = None
    stream_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    stream_url: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class CameraResponse(BaseModel):
    id: int
    name: str
    location: Optional[str] = None
    stream_url: Optional[str] = None
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
