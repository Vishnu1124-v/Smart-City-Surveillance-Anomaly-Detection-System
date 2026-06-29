from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.utils.auth import get_password_hash

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    if db.query(Category).first():
        print("Database already seeded")
        db.close()
        return

    admin = User(
        email="admin@urbaneve.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        is_admin=True,
    )
    db.add(admin)
    db.commit()

    categories_data = [
        {"name": "Dresses", "description": "Elegant dresses for every occasion"},
        {"name": "Tops", "description": "Stylish tops and blouses"},
        {"name": "Bottoms", "description": "Pants, skirts, and shorts"},
        {"name": "Outerwear", "description": "Jackets, coats, and hoodies"},
        {"name": "Accessories", "description": "Bags, jewelry, and more"},
        {"name": "Footwear", "description": "Shoes, boots, and sneakers"},
    ]

    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        db.commit()
        db.refresh(category)
        categories[cat_data["name"]] = category

    products_data = [
        {"name": "Floral Summer Dress", "description": "Light and breezy floral dress perfect for summer days", "price": 59.99, "stock": 25, "category": "Dresses", "image_url": "/images/floral-dress.jpg"},
        {"name": "Little Black Dress", "description": "Classic little black dress for any formal event", "price": 89.99, "stock": 30, "category": "Dresses", "image_url": "/images/black-dress.jpg"},
        {"name": "Striped Cotton Top", "description": "Comfortable striped cotton top for casual wear", "price": 34.99, "stock": 50, "category": "Tops", "image_url": "/images/striped-top.jpg"},
        {"name": "Silk Blouse", "description": "Luxurious silk blouse in cream", "price": 69.99, "stock": 20, "category": "Tops", "image_url": "/images/silk-blouse.jpg"},
        {"name": "High-Waist Jeans", "description": "Trendy high-waist denim jeans", "price": 49.99, "stock": 35, "category": "Bottoms", "image_url": "/images/high-waist-jeans.jpg"},
        {"name": "Pleated Midi Skirt", "description": "Elegant pleated midi skirt in navy", "price": 44.99, "stock": 28, "category": "Bottoms", "image_url": "/images/pleated-skirt.jpg"},
        {"name": "Denim Jacket", "description": "Classic denim jacket with a modern fit", "price": 79.99, "stock": 15, "category": "Outerwear", "image_url": "/images/denim-jacket.jpg"},
        {"name": "Wool Coat", "description": "Warm wool coat for winter", "price": 149.99, "stock": 10, "category": "Outerwear", "image_url": "/images/wool-coat.jpg"},
        {"name": "Leather Crossbody Bag", "description": "Genuine leather crossbody bag", "price": 59.99, "stock": 40, "category": "Accessories", "image_url": "/images/crossbody-bag.jpg"},
        {"name": "Gold Hoop Earrings", "description": "14k gold hoop earrings set", "price": 29.99, "stock": 100, "category": "Accessories", "image_url": "/images/gold-hoops.jpg"},
        {"name": "White Sneakers", "description": "Classic white leather sneakers", "price": 74.99, "stock": 45, "category": "Footwear", "image_url": "/images/white-sneakers.jpg"},
        {"name": "Ankle Boots", "description": "Chic black ankle boots with block heel", "price": 99.99, "stock": 22, "category": "Footwear", "image_url": "/images/ankle-boots.jpg"},
    ]

    for prod_data in products_data:
        category_name = prod_data.pop("category")
        product = Product(category_id=categories[category_name].id, **prod_data)
        db.add(product)

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
