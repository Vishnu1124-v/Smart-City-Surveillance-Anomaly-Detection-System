from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.services.alert_service import AlertService
from app.services.detection_service import DetectionService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    svc: AlertService = Depends(),
):
    return svc.get_all(status, severity)


@router.get("/stats")
def alert_stats(svc: AlertService = Depends()):
    return svc.get_stats()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, svc: AlertService = Depends()):
    return svc.get_by_id(alert_id)


@router.post("/", response_model=AlertResponse)
def create_alert(data: AlertCreate, svc: AlertService = Depends(), user: User = Depends(get_current_user)):
    return svc.create(data)


@router.post("/scan")
def scan_cameras(svc: DetectionService = Depends(), user: User = Depends(get_current_user)):
    alerts = svc.scan_all_cameras()
    return {"alerts_detected": len(alerts)}


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, data: AlertUpdate, svc: AlertService = Depends(), user: User = Depends(get_current_user)):
    return svc.update(alert_id, data)
