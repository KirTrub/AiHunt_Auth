from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    email: EmailStr
    
    password: str
    password_repeated: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    email: EmailStr
    role_id: int

    model_config = {"from_attributes": True}