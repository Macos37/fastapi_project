from pydantic import BaseModel, EmailStr
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from typing import Optional


class UserRead(BaseUser[int], BaseModel):
    id: int
    email: EmailStr
    

    class Config:
        orm_mode = True

 
class UserCreate(BaseUserCreate):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
  
  
class UserUpdate(BaseUserUpdate):
    email: Optional[EmailStr] = None
    
    class Config:
        orm_mode = True
        
    
    

    
    
