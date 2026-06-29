from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import create_access_token, get_password_hash, verify_password


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def register(self, user_data: UserCreate) -> dict:
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        token = create_access_token(data={"sub": user.id})
        return {"access_token": token, "token_type": "bearer"}

    def login(self, username: str, password: str) -> dict:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.id})
        return {"access_token": token, "token_type": "bearer"}
