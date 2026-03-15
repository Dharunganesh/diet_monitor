from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Secret key for JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(BaseModel):
    username: str
    password: str


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Hash password
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


# Verify password
def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Register
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


# Login
@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):

    db_user = db.query(models.Registration).filter(
        models.Registration.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Create JWT token
    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "message":"login successfull",
        "access_token": access_token,
        "token_type": "bearer"
    }
