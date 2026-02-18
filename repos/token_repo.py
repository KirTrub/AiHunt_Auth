from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.black_list import BlacklistedToken
from models.refresh_token import RefreshToken

class ITokenRepository(ABC):
    @abstractmethod
    async def add_refresh_token(self, user_id: int, token: str, expires_at: datetime):
        pass

    @abstractmethod
    async def get_refresh_token(self, token: str) -> RefreshToken:
        pass

    @abstractmethod
    async def delete_refresh_token(self, token: str):
        pass

    @abstractmethod
    async def blacklist_access_token(self, jti: str, expires_at: datetime):
        pass

    @abstractmethod
    async def is_blacklisted(self, jti: str) -> bool:
        pass

class TokenRepositoryImpl(ITokenRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def add_refresh_token(self, user_id: int, token: str, expires_at: datetime):
        db_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        self.db.add(db_token)
        await self.db.commit()

    async def get_refresh_token(self, token: str) -> RefreshToken:
        res = await self.db.execute(select(RefreshToken).where(RefreshToken.token == token))
        return res.scalar_one_or_none()

    async def delete_refresh_token(self, token: str):
        await self.db.execute(delete(RefreshToken).where(RefreshToken.token == token))
        await self.db.commit()

    async def blacklist_access_token(self, jti: str, expires_at: datetime):
        self.db.add(BlacklistedToken(jti=jti, expires_at=expires_at))
        await self.db.commit()

    async def is_blacklisted(self, jti: str) -> bool:
        res = await self.db.execute(select(BlacklistedToken).where(BlacklistedToken.jti == jti))
        return res.scalar_one_or_none() is not None