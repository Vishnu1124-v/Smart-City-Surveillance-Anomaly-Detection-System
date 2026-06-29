from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate


class AlertService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, status: Optional[str] = None, severity: Optional[str] = None) -> List[Alert]:
        q = self.db.query(Alert)
        if status:
            q = q.filter(Alert.status == status)
        if severity:
            q = q.filter(Alert.severity == severity)
        return q.order_by(Alert.created_at.desc()).all()

    def get_by_id(self, alert_id: int) -> Alert:
        a = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Alert not found")
        return a

    def create(self, data: AlertCreate) -> Alert:
        alert = Alert(**data.model_dump())
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def update(self, alert_id: int, data: AlertUpdate) -> Alert:
        alert = self.get_by_id(alert_id)
        for f, v in data.model_dump(exclude_unset=True).items():
            setattr(alert, f, v)
        if data.status == "resolved":
            alert.resolved_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_stats(self) -> dict:
        total = self.db.query(Alert).count()
        open_count = self.db.query(Alert).filter(Alert.status == "open").count()
        high = self.db.query(Alert).filter(Alert.severity == "high").count()
        return {"total": total, "open": open_count, "high_severity": high}
