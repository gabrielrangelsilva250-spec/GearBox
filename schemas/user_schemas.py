from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True