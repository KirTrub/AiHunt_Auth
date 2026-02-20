from abc import ABC, abstractmethod
from typing import List
from exceptions.exceptions import NotFoundException
from models.permissions import Permission
from dto.Permission import PermissionCreate, PermissionUpdate
from repos.permission_repo import IPermissionRepository

class IPermissionService(ABC):
    @abstractmethod
    async def create(self, data: PermissionCreate) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, permission_id: int) -> Permission:
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

class PermissionServiceImpl(IPermissionService):
    def __init__(self, permission_repo: IPermissionRepository):
        self.permission_repo = permission_repo

    async def create(self, data: PermissionCreate) -> int:
        return await self.permission_repo.create(data)

    async def get_by_id(self, permission_id: int) -> Permission:
        permission = await self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise NotFoundException()
        return permission
    
    async def get_by_role_id_and_resource_name(self, role_id: int, resource_name: str) -> Permission:
        permission = await self.permission_repo.get_by_role_id_and_resource_name(role_id, resource_name)
        if not permission:
            raise NotFoundException()
        return permission
    

    async def get_all(self) -> List[Permission]:
        return await self.permission_repo.get_all()

    async def update(self, permission_id: int, data: PermissionUpdate) -> Permission:
        updated = await self.permission_repo.update(permission_id, data)
        if not updated:
            raise NotFoundException()
        return updated

    async def delete_by_id(self, permission_id: int) -> int:
        deleted_id = await self.permission_repo.delete_by_id(permission_id)
        if not deleted_id:
            raise NotFoundException()
        return deleted_id
