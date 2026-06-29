from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.models.user import User
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate
from app.schemas.recording import RecordingResponse
from app.services.camera_service import CameraService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.get("/", response_model=List[CameraResponse])
def list_cameras(status: Optional[str] = Query(None), svc: CameraService = Depends()):
    return svc.get_all(status)


@router.get("/stats")
def camera_stats(svc: CameraService = Depends()):
    return svc.get_stats()


@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(camera_id: int, svc: CameraService = Depends()):
    return svc.get_by_id(camera_id)


@router.post("/", response_model=CameraResponse)
def create_camera(data: CameraCreate, svc: CameraService = Depends(), user: User = Depends(get_current_user)):
    return svc.create(data)


@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera(camera_id: int, data: CameraUpdate, svc: CameraService = Depends(), user: User = Depends(get_current_user)):
    return svc.update(camera_id, data)


@router.delete("/{camera_id}")
def delete_camera(camera_id: int, svc: CameraService = Depends(), user: User = Depends(get_current_user)):
    svc.delete(camera_id)
    return {"message": "Camera deleted"}
