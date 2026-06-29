from typing import List

from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate
from app.services.cart_service import CartService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("/", response_model=List[CartItemResponse])
def get_cart(
    cart_service: CartService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return cart_service.get_cart(current_user)


@router.post("/", response_model=CartItemResponse)
def add_to_cart(
    data: CartItemCreate,
    cart_service: CartService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return cart_service.add_item(current_user, data)


@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    cart_service: CartService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return cart_service.update_item(current_user, item_id, data)


@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    cart_service: CartService = Depends(),
    current_user: User = Depends(get_current_user),
):
    cart_service.remove_item(current_user, item_id)
    return {"message": "Item removed from cart"}
