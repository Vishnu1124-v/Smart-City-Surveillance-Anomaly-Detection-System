from typing import List

from fastapi import APIRouter, Depends

from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
def list_categories(category_service: CategoryService = Depends()):
    return category_service.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, category_service: CategoryService = Depends()):
    return category_service.get_by_id(category_id)


@router.post("/", response_model=CategoryResponse)
def create_category(
    data: CategoryCreate,
    category_service: CategoryService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return category_service.create(data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    category_service: CategoryService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return category_service.update(category_id, data)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(),
    current_user: User = Depends(get_current_user),
):
    category_service.delete(category_id)
    return {"message": "Category deleted"}
