from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    email: EmailStr
    
    password: str
    password_repeated: str
