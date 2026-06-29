from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_orders(self, user: User) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user.id).all()

    def get_by_id(self, user: User, order_id: int) -> Order:
        order = self.db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user.id,
        ).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def create_from_cart(self, user: User, data: OrderCreate) -> Order:
        cart_items = self.db.query(CartItem).filter(CartItem.user_id == user.id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total = 0.0
        order_items = []
        for cart_item in cart_items:
            product = self.db.query(Product).filter(Product.id == cart_item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} not found")
            if product.stock < cart_item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

            product.stock -= cart_item.quantity
            item_total = product.price * cart_item.quantity
            total += item_total
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=cart_item.quantity,
                price=product.price,
            ))

        order = Order(
            user_id=user.id,
            total=total,
            shipping_address=data.shipping_address,
            items=order_items,
        )
        self.db.add(order)
        self.db.query(CartItem).filter(CartItem.user_id == user.id).delete()
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order_id: int, status: str) -> Order:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
