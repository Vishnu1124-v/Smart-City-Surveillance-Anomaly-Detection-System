from app.api.auth import router as auth_router
from app.api.cameras import router as cameras_router
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router

__all__ = ["auth_router", "cameras_router", "alerts_router", "dashboard_router"]
