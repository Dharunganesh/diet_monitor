from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt

import models
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Request model
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
    return hashed.decode('utf-8')


# Verify password
def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# Register API
@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(models.Registration).filter(
        models.Registration.username == user.username
    ).first()

    if existing_user:
        return {"message": "User already exists"}

    # Hash password
    hashed_password = hash_password(user.password)

    # Save user in database
    new_user = models.Registration(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# Login API
@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):

    db_user = db.query(models.Registration).filter(
        models.Registration.username == user.username
    ).first()

    if not db_user:
        return {"message": "User not found"}

    if verify_password(user.password, db_user.password):
        return {"message": "Login successful"}

    return {"message": "Invalid password"}