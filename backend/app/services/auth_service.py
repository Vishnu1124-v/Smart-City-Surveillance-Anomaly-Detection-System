from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import create_token, hash_password, verify_password


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def register(self, data: UserCreate) -> dict:
        if self.db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.db.query(User).filter(User.username == data.username).first():
            raise HTTPException(status_code=400, detail="Username taken")
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {"access_token": create_token(data={"sub": user.id}), "token_type": "bearer"}

    def login(self, username: str, password: str) -> dict:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": create_token(data={"sub": user.id}), "token_type": "bearer"}
