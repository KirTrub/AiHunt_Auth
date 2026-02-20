from pydantic import BaseModel
from typing import Optional

class ArticleCreate(BaseModel):
    name: str
    text: str
    owner_id: Optional[int] = None

class ArticleUpdate(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    owner_id: Optional[int] = None

class ArticleResponse(BaseModel):
    id: int
    name: str
    text: str
    owner_id: int