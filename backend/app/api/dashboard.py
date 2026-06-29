from fastapi import APIRouter, Depends

from app.models.user import User
from app.services.alert_service import AlertService
from app.services.camera_service import CameraService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/")
def dashboard(cam_svc: CameraService = Depends(), alert_svc: AlertService = Depends(), user: User = Depends(get_current_user)):
    return {
        "cameras": cam_svc.get_stats(),
        "alerts": alert_svc.get_stats(),
        "recent_alerts": [
            {
                "id": a.id,
                "title": a.title,
                "severity": a.severity,
                "status": a.status,
                "camera_name": a.camera.name if a.camera else None,
                "created_at": a.created_at.isoformat(),
            }
            for a in alert_svc.get_all(status="open")[:5]
        ],
    }
