import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_router, users_router, categories_router, products_router, cart_router, orders_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Urbaneve API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        *(f"https://{os.environ['VERCEL_URL']}" for _ in [1] if os.environ.get("VERCEL_URL")),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
