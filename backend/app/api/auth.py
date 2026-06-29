from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import Token, UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(data: UserCreate, svc: AuthService = Depends()):
    return svc.register(data)


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), svc: AuthService = Depends()):
    return svc.login(form.username, form.password)


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
