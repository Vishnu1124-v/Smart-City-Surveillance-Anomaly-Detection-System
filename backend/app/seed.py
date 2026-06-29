from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.camera import Camera
from app.models.alert import Alert
from app.utils.auth import hash_password

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    if db.query(Camera).first():
        print("Database already seeded")
        db.close()
        return

    admin = User(
        email="admin@urbaneye.com",
        username="admin",
        hashed_password=hash_password("admin123"),
        full_name="System Admin",
        role="admin",
    )
    operator = User(
        email="operator@urbaneye.com",
        username="operator",
        hashed_password=hash_password("operator123"),
        full_name="Camera Operator",
        role="operator",
    )
    db.add_all([admin, operator])
    db.commit()
    db.refresh(admin)
    db.refresh(operator)

    cameras_data = [
        {"name": "Main Entrance - North Gate", "location": "North Gate, Sector 1", "status": "online", "latitude": 12.9716, "longitude": 77.5946},
        {"name": "South Junction - Traffic Cam", "location": "South Junction, Sector 3", "status": "online", "latitude": 12.9352, "longitude": 77.6245},
        {"name": "Central Square - Plaza", "location": "Central Square, Sector 2", "status": "online", "latitude": 12.9580, "longitude": 77.6140},
        {"name": "East Corridor - Metro Exit", "location": "East Metro Exit, Sector 4", "status": "offline", "latitude": 12.9870, "longitude": 77.6500},
        {"name": "West Parking Lot", "location": "West Parking, Sector 1", "status": "online", "latitude": 12.9650, "longitude": 77.5800},
        {"name": "Market Street Surveillance", "location": "Market Street, Sector 2", "status": "online", "latitude": 12.9700, "longitude": 77.6000},
    ]

    cameras = {}
    for cam_data in cameras_data:
        cam = Camera(**cam_data)
        db.add(cam)
        db.commit()
        db.refresh(cam)
        cameras[cam_data["name"]] = cam

    alerts_data = [
        {"camera": "Main Entrance - North Gate", "title": "Suspicious Movement Detected", "description": "Unauthorized vehicle approach at north gate", "severity": "high", "anomaly_type": "suspicious_movement", "confidence": 0.92, "status": "open", "assigned_to": admin.id},
        {"camera": "Central Square - Plaza", "title": "Crowd Formation Alert", "description": "Unusual crowd gathering detected in central plaza", "severity": "medium", "anomaly_type": "crowd_formation", "confidence": 0.78, "status": "open"},
        {"camera": "Market Street Surveillance", "title": "Object Abandoned", "description": "Suspicious package left at market street bench", "severity": "high", "anomaly_type": "object_abandoned", "confidence": 0.85, "status": "open"},
        {"camera": "South Junction - Traffic Cam", "title": "Traffic Anomaly", "description": "Vehicle stopped in restricted zone", "severity": "medium", "anomaly_type": "loitering", "confidence": 0.71, "status": "open"},
    ]

    for alert_data in alerts_data:
        camera_name = alert_data.pop("camera")
        alert = Alert(camera_id=cameras[camera_name].id, **alert_data)
        db.add(alert)

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
