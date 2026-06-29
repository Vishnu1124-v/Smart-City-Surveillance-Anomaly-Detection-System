from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Category:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def create(self, data: CategoryCreate) -> Category:
        if self.db.query(Category).filter(Category.name == data.name).first():
            raise HTTPException(status_code=400, detail="Category already exists")
        category = Category(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.get_by_id(category_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        self.db.delete(category)
        self.db.commit()
