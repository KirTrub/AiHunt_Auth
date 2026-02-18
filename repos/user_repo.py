from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from dto.UserUpdate import UserUpdate
from dto.UserCreate import UserCreate
from models.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, last_name: str,
                            first_name: str,
                            patronymic: str,
                            email: str,
                            password_hashed: str) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def get_all(self, ) -> User:
        pass
    
    @abstractmethod
    async def update(self, id: int, data: UserUpdate) -> User:
        pass
    
    @abstractmethod
    async def delete_by_id(self, id: int) -> int:
        pass

class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create(self, last_name: str,
                            first_name: str,
                            patronymic: str,
                            email: str,
                            password_hashed: str) -> int:
        user = User(last_name = last_name,
                    first_name = first_name,
                    patronymic = patronymic,
                    email = email,
                    password_hashed = password_hashed
                    )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user.id

    async def get_by_id(self, id: int) -> User:
        result = await self.db.execute(select(User).where(User.id==id).where(User.is_active==True))
        user = result.scalar_one()
        if not user:
            return None
        return user
    
    async def get_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).where(User.email==email).where(User.is_active==True))
        user = result.scalar_one()
        if not user:
            return None
        return user

    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(User).where(User.is_active==True))
        users = result.scalars().all()
        if not users:
            return []
        
        return users
    

    async def update(self, id: int, data: UserUpdate) -> User:
        result = await self.db.execute(select(User).where(User.id==id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        
        updates = data.model_dump(exclude_unset=True)
        
        for key, value in updates.items():
            setattr(user, key, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def safe_delete_by_id(self, id: int) -> int:
        result = await self.db.execute(select(User).where(User.id==id).where(User.is_active==True))
        user = result.scalar_one_or_none()

        if not user:
            return None
        
        user.is_active=False

        await self.db.commit()
        await self.db.refresh(user)
        return user.id
   
