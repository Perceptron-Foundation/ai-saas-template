from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
import jwt

from Backend_py.core.config import settings
from Backend_py.database.db import SessionLocal
from Backend_py.database import crud, model

# session creation for every request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

# get current active user dependency
# authentication and authorization


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_email(db, email=email)  
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: model.User = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


