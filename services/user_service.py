from abc import ABC, abstractmethod
from typing import List

from dto.UserCreate import UserCreate
from dto.UserUpdate import UserUpdate
from exceptions.exceptions import DifferingPasswordsException, EmailAlreadyExistsException, NotFoundException
from models.user import User
from repos.token_repo import ITokenRepository
from repos.user_repo import IUserRepository
from security import hash_password


class IUserService(ABC):
    @abstractmethod
    async def create(self, data: UserCreate) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def update(self, user_id: int, data: UserUpdate) -> User:
        pass

    @abstractmethod
    async def soft_delete_by_id(self, user_id: int) -> int:
        pass

class UserServiceImpl(IUserService):
    def __init__(self, token_repo: ITokenRepository, 
                 user_repo: IUserRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def create(self, data:UserCreate) -> int:
        db_email = await self.user_repo.get_by_email(data.email)
        if db_email:
            raise EmailAlreadyExistsException()
        if data.password != data.password_repeated:
            raise DifferingPasswordsException()
        
        password_hashed = hash_password(data.password)

        new_user_id = await self.user_repo.create(
            last_name=data.last_name,
            first_name=data.first_name,
            patronymic=data.patronymic,
            email=data.email,
            password_hashed=password_hashed
        )

        return new_user_id
    
    async def get_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException()
        return user
    
    async def get_by_email(self, email: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise NotFoundException()
        return user
        
    async def get_all(self) -> List[User]:
        users = await self.user_repo.get_all()
        return users
    
    async def update(self, user_id: int, data: UserUpdate) -> User:
        updated_user = await self.user_repo.update(user_id, data)
        if not updated_user:
            raise NotFoundException()
        return updated_user
    
    async def soft_delete_by_id(self, user_id) -> int:
        deleted_user_id = await self.user_repo.soft_delete_by_id(user_id)
        if not deleted_user_id:
            raise NotFoundException()
        return deleted_user_id
