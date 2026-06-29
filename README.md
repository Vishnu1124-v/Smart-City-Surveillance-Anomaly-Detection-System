# UrbanEye: Smart City Surveillance & Anomaly Detection System

An intelligent surveillance platform for smart cities that monitors camera feeds, detects anomalies in real-time, and provides a centralized control dashboard for security operators.

## Tech Stack
- **Backend**: FastAPI (Python), SQLAlchemy, PostgreSQL/SQLite
- **Frontend**: React 19, TypeScript, Vite
- **Auth**: JWT-based authentication with bcrypt
- **Deployment**: Vercel (serverless)

## Features
- Real-time camera monitoring and status management
- AI-powered anomaly detection (suspicious movement, unauthorized access, crowd formation, object abandonment, loitering)
- Centralized alert dashboard with severity levels
- Camera network overview with online/offline tracking
- Role-based access (admin, operator)
- RESTful API with automatic database migrations

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
- `POST /api/auth/login` - Login (OAuth2 form)
- `GET /api/auth/me` - Current user profile
- `GET /api/cameras/` - List all cameras
- `GET /api/cameras/stats` - Camera statistics
- `GET/POST/PUT/DELETE /api/cameras/:id` - Camera CRUD
- `GET /api/alerts/` - List alerts (filter by ?status=&severity=)
- `GET /api/alerts/stats` - Alert statistics
- `POST /api/alerts/scan` - Trigger anomaly scan on all cameras
- `PUT /api/alerts/:id` - Update alert (resolve, assign)
- `GET /api/dashboard/` - Dashboard summary

## Seed Data
Run `python -m app.seed` to populate:
- **Admin**: `admin` / `admin123`
- **Operator**: `operator` / `operator123`
- 6 cameras (4 online, 2 offline) across city sectors
- 4 sample anomaly alerts

## Architecture
```
urbaneye/
├── backend/
│   ├── app/
│   │   ├── api/         # FastAPI routers
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic + detection engine
│   │   ├── utils/       # Auth utilities
│   │   ├── config.py    # Settings
│   │   ├── database.py  # DB connection
│   │   ├── main.py      # FastAPI app
│   │   └── seed.py      # Database seeder
│   ├── alembic/         # Migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/         # API client & types
│   │   ├── components/  # Layout
│   │   ├── hooks/       # Auth hooks
│   │   ├── pages/       # Dashboard, Cameras, Alerts, Login
│   │   └── styles/      # CSS
│   └── package.json
├── api/index.py         # Vercel serverless entry
├── vercel.json
└── README.md
```
