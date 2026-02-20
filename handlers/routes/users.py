import http
from typing import List
from fastapi import APIRouter, Depends


from dto.User import UserCreate, UserResponse, UserUpdate
from exceptions.exceptions import NotFoundException
from handlers.deps import Checker, get_user_service
from models.user import User
from services.user_service import IUserService


users_router = APIRouter(prefix="/users")

@users_router.get("", status_code=http.HTTPStatus.OK, response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(Checker(resource_name="user", action="read_all")),
                        user_service: IUserService = Depends(get_user_service)):
    users = await user_service.get_all()
    return users

@users_router.get("/{user_id}", status_code=http.HTTPStatus.OK, response_model=UserResponse)
async def get_user_by_id(user_id: int,
                          current_user: User = Depends(Checker(resource_name="user", action="read")),
                          user_service: IUserService = Depends(get_user_service)):
    db_user = await user_service.get_by_id(user_id)

    if not db_user:
        raise NotFoundException()
    
    return db_user

@users_router.post("", status_code=http.HTTPStatus.CREATED)
async def create_user(data: UserCreate, user_service: IUserService = Depends(get_user_service)):
    new_user_id = await user_service.create(data)
    return new_user_id
    
@users_router.patch("/{user_id}", status_code=http.HTTPStatus.OK, response_model=UserResponse)
async def update_user(user_id: int,
                       data: UserUpdate,
                         user_service: IUserService = Depends(get_user_service),
                         current_user: User = Depends(Checker(resource_name="user", action="update"))):
    user = await user_service.update(user_id, data)
    return user

@users_router.delete("/{user_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def soft_delete_by_id(user_id: int,
                            current_user: User = Depends(Checker(resource_name="user", action="delete")), 
                            user_service: IUserService = Depends(get_user_service)):
    deleted_id = await user_service.soft_delete_by_id(user_id)

    return deleted_id
