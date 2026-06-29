# Smart City Surveillance - Anomaly Detection System

## Overview
An intelligent surveillance system for smart cities that detects anomalies in real-time video feeds using computer vision and deep learning.

## Tech Stack
- **Backend**: FastAPI (Python), SQLAlchemy, SQLite
- **Frontend**: React 19, TypeScript, Vite
- **Auth**: JWT-based authentication with bcrypt

## Features
- Real-time anomaly detection in surveillance video
- User authentication and role-based access
- Product/category management (sample e-commerce module)
- Shopping cart and order processing
- RESTful API with automatic migrations (Alembic)

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/products/` - List products
- `GET /api/products/:id` - Product detail
- `GET /api/categories/` - List categories
- `GET/POST /api/cart/` - Manage cart
- `GET/POST /api/orders/` - Manage orders
- `GET /api/users/me` - Current user

## Seed Data
Run `python -m app.seed` to populate the database with sample categories, products, and an admin user.
- Admin login: `admin` / `admin123`
