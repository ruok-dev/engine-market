from fastapi import APIRouter
from app.api.v1.endpoints import products, sales, inventory, finance, login

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(finance.router, prefix="/finance", tags=["finance"])
