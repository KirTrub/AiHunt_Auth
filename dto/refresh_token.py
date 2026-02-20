from pydantic import BaseModel, EmailStr
from typing import Optional

class RefreshTokenRequest(BaseModel):
    refresh_token: str