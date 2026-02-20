import http
from typing import List
from fastapi import APIRouter, Depends
from dto.Article import ArticleCreate, ArticleResponse, ArticleUpdate
from exceptions.exceptions import NotFoundException
from handlers.deps import Checker, get_article_service
from models.article import Article
from models.user import User
from services.article_service import IArticleService


articles_router = APIRouter(prefix="/articles")

@articles_router.get("", status_code=http.HTTPStatus.OK, response_model=List[ArticleResponse])
async def get_all_articles(current_user: User = Depends(Checker(resource_name="article", action="read_all")),
                        article_service: IArticleService = Depends(get_article_service)):
    articles = await article_service.get_all()
    return articles

@articles_router.get("/{article_id}", status_code=http.HTTPStatus.OK, response_model=ArticleResponse)
async def get_article_by_id(article_id: int,
                          current_user: User = Depends(Checker(resource_name="article", action="read")),
                          article_service: IArticleService = Depends(get_article_service)):
    article = await article_service.get_by_id(article_id)
    if not article:
        raise NotFoundException()
    
    return article

@articles_router.post("", status_code=http.HTTPStatus.CREATED)
async def create_article(data: ArticleCreate,
                      current_user: User = Depends(Checker(resource_name="article", action="create")),
                      article_service: IArticleService = Depends(get_article_service)):
    if current_user.role_id != 1 or data.owner_id is None:
        data.owner_id = current_user.id
    new_article_id = await article_service.create(data)
    return new_article_id
    
@articles_router.patch("/{article_id}", status_code=http.HTTPStatus.OK, response_model=ArticleResponse)
async def update_article(article_id: int,
                       data: ArticleUpdate,
                         article_service: IArticleService = Depends(get_article_service),
                         current_user: User = Depends(Checker(resource_name="article", action="update"))):
    article = await article_service.update(article_id, data)
    return article

@articles_router.delete("/{article_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def delete_by_id(article_id: int,
                            current_user: User = Depends(Checker(resource_name="article", action="delete")), 
                            article_service: IArticleService = Depends(get_article_service)):
    deleted_id = await article_service.delete_by_id(article_id)

    return deleted_id

