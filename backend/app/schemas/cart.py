from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: "ProductResponse" = None

    model_config = {"from_attributes": True}


from app.schemas.product import ProductResponse
CartItemResponse.model_rebuild()
