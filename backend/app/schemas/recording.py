from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecordingResponse(BaseModel):
    id: int
    camera_id: int
    file_url: Optional[str] = None
    duration: float
    file_size: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
