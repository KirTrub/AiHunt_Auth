from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.users import users_router
from .routes.products import products_router
from .routes.articles import articles_router
from .routes.auth import auth_route
from db.seed import seed_all

@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_all() 
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(products_router)
app.include_router(articles_router)
app.include_router(auth_route)