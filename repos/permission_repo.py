from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.permission import Permission
from dto.permission import PermissionCreate, PermissionUpdate
from models.resource import Resource

class IPermissionRepository(ABC):
    @abstractmethod
    async def create(self, data: PermissionCreate) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, permission_id: int) -> Permission:
        pass

    @abstractmethod
    async def get_by_role_id(self, role_id: int):
        pass

    @abstractmethod
    async def get_by_role_id_and_resource_name(self, role_id: int, resource_name: str) -> Permission:
        pass

    @abstractmethod
    async def get_all(self) -> List[Permission]:
        pass

    @abstractmethod
    async def update(self, permission_id: int, data: PermissionUpdate) -> Permission:
        pass

    @abstractmethod
    async def delete_by_id(self, permission_id: int) -> int:
        pass

class PermissionRepositoryImpl(IPermissionRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create(self, data: PermissionCreate) -> int:
        permission = Permission(**data.model_dump())
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission.id

    async def get_by_id(self, permission_id: int) -> Permission:
        result = await self.db.execute(select(Permission).where(Permission.id == permission_id))
        return result.scalar_one_or_none()
    

    async def get_by_role_id(self, role_id: int) -> Permission:
        result = await self.db.execute(select(Permission).where(Permission.role_id == role_id))
        return result.scalar_one_or_none()
    
    async def get_by_role_id_and_resource_name(self, role_id: int, resource_name: str) -> Permission:
        result = await self.db.execute(select(Permission)
                                       .join(Permission.resource_rel)
                                       .where(Permission.role_id == role_id)
                                       .where(Resource.name==resource_name))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Permission]:
        result = await self.db.execute(select(Permission))
        return list(result.scalars().all())

    async def update(self, permission_id: int, data: PermissionUpdate) -> Permission:
        result = await self.db.execute(select(Permission).where(Permission.id == permission_id))
        permission = result.scalar_one_or_none()
        if not permission:
            return None
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(permission, key, value)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def delete_by_id(self, permission_id: int) -> int:
        result = await self.db.execute(select(Permission).where(Permission.id == permission_id))
        permission = result.scalar_one_or_none()
        if not permission:
            return None
        await self.db.delete(permission)
        await self.db.commit()
        return permission_id
