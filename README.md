# 🥗 AI-Based Calorie Tracker

## Tech Stack
- Frontend: React
- Backend: FastAPI
- ML: PyTorch (MobileNetV2)
- Database: PostgreSQL (Neon DB)
- Auth: JWT + bcrypt

## Team
| Role | Name | Tech |
|------|------|------|
| Frontend | Fazil | React |
| Backend | Harrison | FastAPI |
| ML | Dharun | PyTorch |
| Database | Ajay | PostgreSQL |

## Branch Strategy
- `main` → stable production code
- `dev` → integration branch
- `feature/*` → individual feature work

## Setup Instructions
### Database
- Hosted on Neon DB
- Ask Ajay for DATABASE_URL
- Add it to your .env file

### Backend
1. cd backend
2. pip install -r requirements.txt
3. uvicorn main:app --reload

### Frontend
1. cd frontend
2. npm install
3. npm start