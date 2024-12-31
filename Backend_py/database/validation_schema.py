from pydantic import BaseModel, EmailStr

# pydantic models for validation
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: str|None = None


# properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# properties to receive via API for user registration
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str|None = None  

class User(UserBase):
    id: int
    class Config:
        orm_mode = True 


        