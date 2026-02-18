from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from exceptions.exceptions import ForbiddenException, NotAuthenticatedException, NotFoundException, UnauthorizedException
from repos.token_repo import ITokenRepository
from repos.user_repo import IUserRepository
from security import check_password, create_access_token, create_refresh_token, create_tokens

class IAuthService(ABC):
    @abstractmethod
    async def login(self, email: str, password: str):
        pass

    @abstractmethod
    async def refresh(self, old_refresh_token: str):
        pass

    @abstractmethod
    async def logout(self, payload: dict, refresh_token):
        pass


class AuthServiceImpl(IAuthService):

    def __init__(self, token_repo: ITokenRepository, 
                 user_repo: IUserRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedException()

        if not check_password(hashed=user.password_hashed, plain=password):
            raise UnauthorizedException()
        
        if not user.is_active:
            raise UnauthorizedException()
        
        access_token=create_access_token(user_id=user.id, email=user.email)
        refresh_token=create_refresh_token(user_id=user.id)

        await self.token_repo.add_refresh_token(user.id, refresh_token, datetime.now() + timedelta(days=7))
        
        return {"access_token": access_token, "refresh_token": refresh_token}


    async def refresh(self, old_refresh_token: str):
        db_token = await self.token_repo.get_refresh_token(token=old_refresh_token)
        if not db_token or db_token.expires_at < datetime.now():
            raise UnauthorizedException()
        
        user = await self.user_repo.get_by_id(db_token.user_id)

        new_access_token = create_access_token(user.id, user.email)

        return {"access_token": new_access_token}
    

    async def logout(self, payload: dict, refresh_token):
        exp = datetime.fromtimestamp(payload["exp"])
        await self.token_repo.blacklist_access_token(payload["jti"], exp)
        await self.token_repo.delete_refresh_token(refresh_token)
