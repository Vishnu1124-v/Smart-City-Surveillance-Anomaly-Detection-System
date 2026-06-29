from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraUpdate


class CameraService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, status: Optional[str] = None) -> List[Camera]:
        q = self.db.query(Camera)
        if status:
            q = q.filter(Camera.status == status)
        return q.all()

    def get_by_id(self, camera_id: int) -> Camera:
        c = self.db.query(Camera).filter(Camera.id == camera_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Camera not found")
        return c

    def create(self, data: CameraCreate) -> Camera:
        cam = Camera(**data.model_dump())
        self.db.add(cam)
        self.db.commit()
        self.db.refresh(cam)
        return cam

    def update(self, camera_id: int, data: CameraUpdate) -> Camera:
        cam = self.get_by_id(camera_id)
        for f, v in data.model_dump(exclude_unset=True).items():
            setattr(cam, f, v)
        self.db.commit()
        self.db.refresh(cam)
        return cam

    def delete(self, camera_id: int) -> None:
        cam = self.get_by_id(camera_id)
        self.db.delete(cam)
        self.db.commit()

    def get_stats(self) -> dict:
        total = self.db.query(Camera).count()
        online = self.db.query(Camera).filter(Camera.status == "online").count()
        offline = self.db.query(Camera).filter(Camera.status == "offline").count()
        return {"total": total, "online": online, "offline": offline}
