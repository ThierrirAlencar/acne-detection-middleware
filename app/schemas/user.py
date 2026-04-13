from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.utils.enums import defaultStatusEnum

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None

class UserCreate(UserBase):
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    status: Optional[defaultStatusEnum] = None

class UserParams(BaseModel):
    id:int

class UserResponse(UserBase):
    id: int
    status: defaultStatusEnum

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True 

class UserPublic(UserResponse):
    pass