from abc import ABC, abstractmethod
from typing import List
from exceptions.exceptions import NotFoundException
from models.article import Article
from repos.article_repo import IArticleRepository
from dto.Article import ArticleCreate, ArticleUpdate

class IArticleService(ABC):
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

class ArticleServiceImpl(IArticleService):
    def __init__(self, article_repo: IArticleRepository):
        self.article_repo = article_repo

    async def create(self, data: ArticleCreate) -> int:
        return await self.article_repo.create(data)

    async def get_by_id(self, article_id: int) -> Article:
        article = await self.article_repo.get_by_id(article_id)
        if not article:
            raise NotFoundException()
        return article

    async def get_all(self) -> List[Article]:
        return await self.article_repo.get_all()

    async def update(self, article_id: int, data: ArticleUpdate) -> Article:
        updated = await self.article_repo.update(article_id, data)
        if not updated:
            raise NotFoundException()
        return updated

    async def delete_by_id(self, article_id: int) -> int:
        deleted_id = await self.article_repo.delete_by_id(article_id)
        if not deleted_id:
            raise NotFoundException()
        return deleted_id
