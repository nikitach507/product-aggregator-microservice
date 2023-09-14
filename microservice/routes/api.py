from fastapi import APIRouter

from microservice.routes import offer_routes, product_routes, auth_routes


api_router = APIRouter()

api_router.include_router(product_routes.router, prefix="/products", tags=["Products"])
api_router.include_router(offer_routes.router, prefix="/offers", tags=["Offers"])
api_router.include_router(auth_routes.router, prefix="/user", tags=["Auth"])
