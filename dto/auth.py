from pydantic import BaseModel, EmailStr
from typing import Optional

class Login(BaseModel):
    email: str
    password: str