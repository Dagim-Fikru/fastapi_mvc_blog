from sqlalchemy.orm import Session
from app.models.user import User
from app.models.post import Post
from fastapi import HTTPException

def signup(db: Session, email: str, password: str):
    from app.repositories.user_repo import get_user_by_email, create_user
    from app.core.security import get_password_hash

    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    return create_user(db, email, hashed_password)

def login(db: Session, email: str, password: str):
    from app.repositories.user_repo import get_user_by_email
    from app.core.security import verify_password, create_access_token

    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return access_token