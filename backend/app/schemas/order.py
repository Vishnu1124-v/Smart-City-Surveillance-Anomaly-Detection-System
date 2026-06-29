from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: "ProductResponse" = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    shipping_address: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    shipping_address: str


from app.schemas.product import ProductResponse
OrderItemResponse.model_rebuild()
