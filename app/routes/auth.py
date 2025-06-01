from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db
from app.services.auth_service import signup, login
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return signup(db, user.email, user.password)

@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    token = login(db, user.email, user.password)
    return {"access_token": token}