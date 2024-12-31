from sqlalchemy.orm import Session

from Backend_py.database.model import User
from Backend_py.database.validation_schema import UserBase, UserCreate, UserRegister

def create_user(db: Session, user: UserCreate)-> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.password,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

