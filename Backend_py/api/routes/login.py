from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import timedelta

from Backend_py.core.security import get_password_hash, create_access_token, verify_password
from Backend_py.database import crud, validation_schema
from Backend_py.api.deps import get_db
from Backend_py.core.config import settings


router = APIRouter(tags=["login"])


@router.post("/signup", response_model=validation_schema.User)
def signup(user: validation_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email= user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user.password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user)


@router.post("/signin", response_model=validation_schema.User)
def signin(user: validation_schema.UserRegister, response: Response, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(db_user.email, expires_delta=access_token_expire)

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, secure=True)
    return {"access_token": access_token, "token_type": "bearer"}