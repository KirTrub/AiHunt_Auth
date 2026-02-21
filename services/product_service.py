from abc import ABC, abstractmethod
from typing import List
from exceptions.exceptions import NotFoundException
from models.product import Product
from repos.product_repo import IProductRepository
from dto.product import ProductCreate, ProductUpdate

class IProductService(ABC):
    @abstractmethod
    async def create(self, data: ProductCreate) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    async def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def update(self, product_id: int, data: ProductUpdate) -> Product:
        pass

    @abstractmethod
    async def delete_by_id(self, product_id: int) -> int:
        pass

class ProductServiceImpl(IProductService):
    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    async def create(self, data: ProductCreate) -> int:
        return await self.product_repo.create(data)

    async def get_by_id(self, product_id: int) -> Product:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException()
        return product

    async def get_all(self) -> List[Product]:
        return await self.product_repo.get_all()

    async def update(self, product_id: int, data: ProductUpdate) -> Product:
        updated = await self.product_repo.update(product_id, data)
        if not updated:
            raise NotFoundException()
        return updated

    async def delete_by_id(self, product_id: int) -> int:
        deleted_id = await self.product_repo.delete_by_id(product_id)
        if not deleted_id:
            raise NotFoundException()
        return deleted_id
