import random
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.models.camera import Camera


class DetectionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def run_detection(self, camera_id: int) -> Alert | None:
        camera = self.db.query(Camera).filter(Camera.id == camera_id).first()
        if not camera or not camera.is_active:
            return None

        anomaly_detected = random.random() < 0.15

        if not anomaly_detected:
            return None

        anomaly_types = ["suspicious_movement", "unauthorized_access", "crowd_formation", "object_abandoned", "loitering"]
        severities = ["low", "medium", "high"]
        anomaly_type = random.choice(anomaly_types)
        severity = random.choices(severities, weights=[0.3, 0.5, 0.2])[0]
        confidence = round(random.uniform(0.6, 0.98), 2)

        alert = Alert(
            camera_id=camera_id,
            title=f"Anomaly Detected: {anomaly_type.replace('_', ' ').title()}",
            description=f"Detection at {camera.name} ({camera.location or 'unknown location'}). Type: {anomaly_type.replace('_', ' ')}.",
            severity=severity,
            anomaly_type=anomaly_type,
            confidence=confidence,
            status="open",
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def scan_all_cameras(self) -> list[Alert]:
        cameras = self.db.query(Camera).filter(Camera.is_active == True).all()
        alerts = []
        for cam in cameras:
            alert = self.run_detection(cam.id)
            if alert:
                alerts.append(alert)
        return alerts
