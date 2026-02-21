from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.article import Article
from dto.article import ArticleCreate, ArticleUpdate

class IArticleRepository(ABC):
    @abstractmethod
    async def create(self, data: ArticleCreate) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, article_id: int) -> Article:
        pass

    @abstractmethod
    async def get_all(self) -> List[Article]:
        pass

    @abstractmethod
    async def update(self, article_id: int, data: ArticleUpdate) -> Article:
        pass

    @abstractmethod
    async def delete_by_id(self, article_id: int) -> int:
        pass

class ArticleRepositoryImpl(IArticleRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create(self, data: ArticleCreate) -> int:
        article = Article(**data.model_dump())
        self.db.add(article)
        await self.db.commit()
        await self.db.refresh(article)
        return article.id

    async def get_by_id(self, article_id: int) -> Article:
        result = await self.db.execute(select(Article).where(Article.id == article_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Article]:
        result = await self.db.execute(select(Article))
        return list(result.scalars().all())

    async def update(self, article_id: int, data: ArticleUpdate) -> Article:
        result = await self.db.execute(select(Article).where(Article.id == article_id))
        article = result.scalar_one_or_none()
        if not article:
            return None
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(article, key, value)
        await self.db.commit()
        await self.db.refresh(article)
        return article

    async def delete_by_id(self, article_id: int) -> int:
        result = await self.db.execute(select(Article).where(Article.id == article_id))
        article = result.scalar_one_or_none()
        if not article:
            return None
        await self.db.delete(article)
        await self.db.commit()
        return article_id
