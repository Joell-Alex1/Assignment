# auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt, jwt, datetime
from jwt_utils import verify_token
from pydantic import BaseModel

router = APIRouter()

SECRET_KEY = "mysecretkey"  # later move this to .env

# -----------------------------
# Pydantic Models for Requests
# -----------------------------
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Signup Endpoint
# -----------------------------
@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    user = User(email=request.email, hashed_password=hashed_pw.decode('utf-8'))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully!"}

# -----------------------------
# Login Endpoint
# -----------------------------
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not bcrypt.checkpw(request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    payload = {
        "sub": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

# -----------------------------
# Get Profile Endpoint
# -----------------------------
@router.get("/profile")
def get_profile(email: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email}

# -----------------------------
# Update Profile Endpoint
# -----------------------------
@router.put("/profile")
def update_profile(new_email: str, email: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = new_email
    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully!"}
