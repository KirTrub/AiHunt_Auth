from fastapi import APIRouter, Depends


from dto.refresh_token import RefreshTokenRequest
from exceptions.exceptions import NotFoundException
from handlers.deps import Checker, get_auth_service, get_payload, get_user_service
from models.user import User
from dto.auth import Login
from services.auth_service import IAuthService
from services.user_service import IUserService


auth_route = APIRouter()

@auth_route.post("/login")
async def login(data: Login, auth_service: IAuthService = Depends(get_auth_service)):
    tokens = await auth_service.login(data.email, data.password)
    return tokens

@auth_route.post("/refresh")
async def refresh_token(data: RefreshTokenRequest,
                        auth_service: IAuthService = Depends(get_auth_service)):
    new_token = await auth_service.refresh(data.refresh_token)

    return new_token

@auth_route.post("/logout")
async def logout(data: RefreshTokenRequest, 
                 payload: dict = Depends(get_payload),
                auth_service: IAuthService = Depends(get_auth_service),
                ):
    await auth_service.logout(payload, data.refresh_token)

    return {"message": "Successfully logged out"}

