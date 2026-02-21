import os
from typing import AsyncGenerator
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exceptions import ForbiddenException, NotFoundException, UnauthorizedException
from db.session import async_session, get_db
from models.article import Article
from models.product import Product
from models.user import User
from repos.token_repo import ITokenRepository, TokenRepositoryImpl
from repos.user_repo import IUserRepository, UserRepositoryImpl
from repos.article_repo import IArticleRepository, ArticleRepositoryImpl
from repos.product_repo import IProductRepository, ProductRepositoryImpl
from repos.permission_repo import IPermissionRepository, PermissionRepositoryImpl
from services.article_service import ArticleServiceImpl, IArticleService
from services.auth_service import AuthServiceImpl, IAuthService
from services.permission_service import PermissionServiceImpl, IPermissionService
from services.product_service import ProductServiceImpl, IProductService
from services.user_service import IUserService, UserServiceImpl

security = HTTPBearer()

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

"""REPOSTIORIES"""
async def get_user_repo(db: AsyncSession = Depends(get_db_session)) -> IUserRepository:
    return UserRepositoryImpl(db)

async def get_article_repo(db: AsyncSession = Depends(get_db_session)) -> IArticleRepository:
    return ArticleRepositoryImpl(db)

async def get_product_repo(db: AsyncSession = Depends(get_db_session)) -> IProductRepository:
    return ProductRepositoryImpl(db)

async def get_permission_repo(db: AsyncSession = Depends(get_db_session)) -> IPermissionRepository:
    return PermissionRepositoryImpl(db)

async def get_token_repo(db: AsyncSession = Depends(get_db_session)) -> ITokenRepository:
    return TokenRepositoryImpl(db)

"""SERVICES"""
async def get_article_service(article_repo: IArticleRepository = Depends(get_article_repo)) -> IArticleService:
    return ArticleServiceImpl(article_repo)

async def get_auth_service(user_repo: IUserRepository = Depends(get_user_repo),
                           token_repo: ITokenRepository = Depends(get_token_repo)) -> IAuthService:
    return AuthServiceImpl(token_repo=token_repo, user_repo=user_repo)

async def get_permission_service(permission_repo: IPermissionRepository = Depends(get_permission_repo)) -> IPermissionService:
    return PermissionServiceImpl(permission_repo)

async def get_product_service(product_repo: IProductRepository = Depends(get_product_repo)) -> IProductService:
    return ProductServiceImpl(product_repo)

async def get_user_service(user_repo: IUserRepository = Depends(get_user_repo),
                           token_repo: ITokenRepository = Depends(get_token_repo)) -> IUserService:
    return UserServiceImpl(user_repo=user_repo, token_repo=token_repo)


"""Jwt helper"""
async def get_payload(data: HTTPAuthorizationCredentials = Depends(security),
                      token_repo: ITokenRepository = Depends(get_token_repo)) -> dict:
    token = data.credentials

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])

        jti = payload.get("jti")
        if jti:
            is_blacklisted = await token_repo.is_blacklisted(jti)
            if is_blacklisted:
                raise UnauthorizedException("Token has been revoked")

        return payload
    
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException()
    except jwt.PyJWTError:
        raise UnauthorizedException()


class Checker:
    def __init__(self, resource_name: str, action: str):
        self.resource_name = resource_name
        self.action = action
        self._models_map = {
            "product": Product,
            "article": Article,
            "user": User
        }

    async def __call__(
        self,
        request: Request,
        payload: dict = Depends(get_payload),
        perm_service: IPermissionService = Depends(get_permission_service),
        db: AsyncSession = Depends(get_db)
    ):
        res = await db.execute(select(User).where(User.id == int(payload["sub"])))
        user = res.scalar_one_or_none()

        if not user or not user.is_active:
            raise NotFoundException()

        permissions = await perm_service.get_by_role_id_and_resource_name(user.role_id, self.resource_name)
        if not permissions:
            raise ForbiddenException()

        if getattr(permissions, f"{self.action}_all_perm", False):
            return user

        if not getattr(permissions, f"{self.action}_perm", False):
            raise ForbiddenException()

        target_id = None
        for key, value in request.path_params.items():
            if key == "id" or key.endswith("_id"):
                try:
                    target_id = int(value)
                    break
                except ValueError:
                    continue

        if target_id is None:
            return user

        if self.resource_name == "user":
            if target_id != user.id:
                raise ForbiddenException("You can only modify your own profile")
        
        else:
            model = self._models_map.get(self.resource_name)
            if model:
                query = select(model).where(model.id == target_id)
                result = await db.execute(query)
                obj = result.scalar_one_or_none()
                
                if not obj:
                    raise NotFoundException(f"{self.resource_name} not found")
                
                actual_owner_id = getattr(obj, "owner_id", None)
                if actual_owner_id != user.id:
                    raise ForbiddenException(f"Not your {self.resource_name}")

        return user