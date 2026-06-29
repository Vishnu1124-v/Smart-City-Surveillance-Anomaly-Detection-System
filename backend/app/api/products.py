from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def list_products(
    category_id: Optional[int] = Query(None),
    product_service: ProductService = Depends(),
):
    return product_service.get_all(category_id)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, product_service: ProductService = Depends()):
    return product_service.get_by_id(product_id)


@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    product_service: ProductService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return product_service.create(data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    product_service: ProductService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return product_service.update(product_id, data)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    product_service: ProductService = Depends(),
    current_user: User = Depends(get_current_user),
):
    product_service.delete(product_id)
    return {"message": "Product deleted"}
