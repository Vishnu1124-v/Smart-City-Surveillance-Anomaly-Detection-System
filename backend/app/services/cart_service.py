from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate


class CartService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_cart(self, user: User) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.user_id == user.id).all()

    def add_item(self, user: User, data: CartItemCreate) -> CartItem:
        product = self.db.query(Product).filter(Product.id == data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        existing = self.db.query(CartItem).filter(
            CartItem.user_id == user.id,
            CartItem.product_id == data.product_id,
        ).first()

        if existing:
            existing.quantity += data.quantity
            self.db.commit()
            self.db.refresh(existing)
            return existing

        cart_item = CartItem(user_id=user.id, **data.model_dump())
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def update_item(self, user: User, item_id: int, data: CartItemUpdate) -> CartItem:
        cart_item = self.db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.user_id == user.id,
        ).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        cart_item.quantity = data.quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_item(self, user: User, item_id: int) -> None:
        cart_item = self.db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.user_id == user.id,
        ).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        self.db.delete(cart_item)
        self.db.commit()

    def clear_cart(self, user: User) -> None:
        self.db.query(CartItem).filter(CartItem.user_id == user.id).delete()
        self.db.commit()
