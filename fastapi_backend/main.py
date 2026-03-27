from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# JWT CONFIG
# -----------------------------
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# -----------------------------
# SCHEMAS
# -----------------------------
class User(BaseModel):
    username: str
    password: str


class PredictionRequest(BaseModel):
    text: str


class EntryCreate(BaseModel):
    title: str
    description: str


# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# PASSWORD FUNCTIONS
# -----------------------------
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# -----------------------------
# CREATE JWT TOKEN
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# -----------------------------
# VERIFY JWT TOKEN
# -----------------------------
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Token invalid")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")


# -----------------------------
# REGISTER
# -----------------------------
@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):

    existing_user = db.query(models.Registration).filter(
        models.Registration.username == user.username
    ).first()

    if existing_user:
        return {"message": "User already exists"}

    hashed_password = hash_password(user.password)

    new_user = models.Registration(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


# -----------------------------
# LOGIN (UPDATED)
# -----------------------------
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(models.Registration).filter(
        models.Registration.username == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -----------------------------
# PROTECTED API
# -----------------------------
@app.post("/api/predict")
def predict(data: PredictionRequest, user: str = Depends(verify_token)):

    result = {
        "input": data.text,
        "prediction": "phishing",
        "confidence": 0.87
    }

    return {
        "message": "Prediction generated successfully",
        "user": user,
        "result": result
    }


# -----------------------------
# CREATE ENTRY
# -----------------------------
@app.post("/api/entry/new")
def create_entry(entry: EntryCreate, user: str = Depends(verify_token)):

    new_entry = {
        "title": entry.title,
        "description": entry.description,
        "created_by": user
    }

    return {
        "message": "Entry created successfully",
        "data": new_entry
    }
