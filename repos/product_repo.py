from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from dto.Product import ProductCreate, ProductUpdate

class IProductRepository(ABC):
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

class ProductRepositoryImpl(IProductRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create(self, data: ProductCreate) -> int:
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product.id

    async def get_by_id(self, product_id: int) -> Product:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return list(result.scalars().all())

    async def update(self, product_id: int, data: ProductUpdate) -> Product:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return None
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_by_id(self, product_id: int) -> int:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return None
        await self.db.delete(product)
        await self.db.commit()
        return product_id
