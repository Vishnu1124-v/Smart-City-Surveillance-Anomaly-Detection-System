from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AlertCreate(BaseModel):
    camera_id: int
    title: str
    description: Optional[str] = None
    severity: str = "medium"
    anomaly_type: Optional[str] = None
    confidence: float = 0.0
    snapshot_url: Optional[str] = None
    assigned_to: Optional[int] = None


class AlertUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[int] = None


class AlertResponse(BaseModel):
    id: int
    camera_id: int
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    anomaly_type: Optional[str] = None
    confidence: float
    snapshot_url: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    camera: Optional["CameraResponse"] = None

    model_config = {"from_attributes": True}


from app.schemas.camera import CameraResponse
AlertResponse.model_rebuild()
