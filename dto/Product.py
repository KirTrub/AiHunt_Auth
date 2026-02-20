from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    owner_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    owner_id: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    owner_id: int

