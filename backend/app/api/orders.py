from typing import List

from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    order_service: OrderService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_orders(current_user)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    order_service: OrderService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_by_id(current_user, order_id)


@router.post("/", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    order_service: OrderService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return order_service.create_from_cart(current_user, data)
