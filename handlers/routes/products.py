import http
from typing import List
from fastapi import APIRouter, Depends

from dto.Product import ProductCreate, ProductResponse, ProductUpdate
from exceptions.exceptions import NotFoundException
from handlers.deps import Checker, get_product_service
from models.product import Product
from models.user import User
from services.product_service import IProductService

products_router = APIRouter(prefix="/products")

@products_router.get("", status_code=http.HTTPStatus.OK, response_model=List[ProductResponse])
async def get_all_products(current_user: User = Depends(Checker(resource_name="product", action="read_all")),
                        product_service: IProductService = Depends(get_product_service)):
    products = await product_service.get_all()
    return products

@products_router.get("/{product_id}", status_code=http.HTTPStatus.OK, response_model=ProductResponse)
async def get_product_by_id(product_id: int,
                          current_user: User = Depends(Checker(resource_name="product", action="read")),
                          product_service: IProductService = Depends(get_product_service)):
    product = await product_service.get_by_id(product_id)
    if not product:
        raise NotFoundException()
    
    return product

@products_router.post("", status_code=http.HTTPStatus.CREATED)
async def create_product(data: ProductCreate,
                      current_user: User = Depends(Checker(resource_name="product", action="create")),
                      product_service: IProductService = Depends(get_product_service)):
    if current_user.role_id != 1 or data.owner_id is None:
        data.owner_id = current_user.id
    
    new_product_id = await product_service.create(data)
    return new_product_id
    
@products_router.patch("/{product_id}", status_code=http.HTTPStatus.OK, response_model=ProductResponse)
async def update_product(product_id: int,
                       data: ProductUpdate,
                         product_service: IProductService = Depends(get_product_service),
                         current_user: User = Depends(Checker(resource_name="product", action="update"))):
    product = await product_service.update(product_id, data)
    return product

@products_router.delete("/{product_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def delete_by_id(product_id: int,
                            current_user: User = Depends(Checker(resource_name="product", action="delete")), 
                            product_service: IProductService = Depends(get_product_service)):
    deleted_id = await product_service.delete_by_id(product_id)

    return deleted_id

