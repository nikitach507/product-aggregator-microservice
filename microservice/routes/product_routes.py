from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from microservice.services.offers import get_product_offer_data
from microservice.services.products import register_product_in_offer_service
from microservice.services.token_manager import token_manager
from microservice.database.database_setup import session
from microservice.models.models import Offer, Product
from microservice.auth.jwt_bearer import JwtBearer

from microservice.utils.logging_configure import get_logger


logger_api = get_logger()


router = APIRouter()


class ProductCreate(BaseModel):
    name: str
    description: str


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str


def create_offer_db(offers_data, product_id: UUID):
    """
    Create Offer database records based on offer data.

    Args:
        offers_data (list[dict]): List of offer data.
        product_id (UUID): ID of the product associated with the offers.
    Returns:
        bool: True if offers were successfully created, False otherwise.
    """
    for offer in offers_data:
        offer_db = Offer(
            id=offer["id"],
            price=offer["price"],
            items_in_stock=offer["items_in_stock"],
            product_id=product_id,
        )
        session.add(offer_db)
    session.commit()
    logger_api.info(f"Successful addition of all offeers for product with id {product_id}.")
    return True


@router.get("/", response_model=list[ProductResponse])
def get_all_products(skip: int = 0, limit: int = 100):
    """
    Get a list of all products.

    Args:
        skip (int): Number of items to skip.
        limit (int): Maximum number of items to return.

    Returns:
        list[ProductResponse]: List of ProductResponse objects.
    """
    try:
        products = session.query(Product).offset(skip).limit(limit).all()
        logger_api.info("Retrieved all products successfully.")
        return products
    except Exception as exc:
        logger_api.exception(f"Error retrieving products: ")
        raise HTTPException(status_code=500, detail="Error retrieving products")


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID):
    """
    Get a product by its ID.

    Args:
        product_id (UUID): ID of the product to retrieve.

    Returns:
        ProductResponse: ProductResponse object.
    """

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger_api.error(f"Product with product id {product_id} does not exist.")
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} does not exist"
        )
    logger_api.info(f"Retrieved product with product id {product_id}.")
    return product


@router.post("/", dependencies=[Depends(JwtBearer())], response_model=ProductResponse)
def create_product(
        product: ProductCreate,
        active_access_token: str = Depends(token_manager.get_access_token)):
    """
    Create a new product.

    Args:
        product (ProductCreate): ProductCreate object with product data.
        active_access_token (str): Active access token obtained from token_manager.

    Returns:
        ProductResponse: ProductResponse object of the newly created product.
    """

    product_db = Product(name=product.name, description=product.description)
    session.add(product_db)
    session.commit()

    if not active_access_token:
        logger_api.error("No active access token available.")
        raise HTTPException(status_code=500, detail="No active access token")

    product_dict = {
        "id": str(product_db.id),
        "name": product_db.name,
        "description": product_db.description,
    }

    register_product = register_product_in_offer_service(
        active_access_token, product_dict
    )

    if not register_product:
        logger_api.error("Error while calling external API.")
        raise HTTPException(status_code=500, detail="Error while calling external API")

    offers_data = get_product_offer_data(active_access_token, product_db.id)

    if create_offer_db(offers_data, product_db.id):
        return product_db
    else:
        logger_api.error("Error with creating offers.")
        raise HTTPException(status_code=500, detail="Error with creating offers")


@router.put("/{product_id}", dependencies=[Depends(JwtBearer())], response_model=ProductResponse)
def update_product(product_id: UUID, new_product: ProductCreate):
    """
    Update a product by its ID.

    Args:
        product_id (UUID): ID of the product to update.
        new_product (ProductCreate): ProductCreate object with updated product data.

    Returns:
        ProductResponse: ProductResponse object of the updated product.
    """

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger_api.error(f"Product with product id {product_id} does not exist.")
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} does not exist"
        )

    product.name = new_product.name
    product.description = new_product.description
    session.commit()

    logger_api.info(f"Updated product with product id {product_id}.")
    return product


@router.delete("/{product_id}", dependencies=[Depends(JwtBearer())], response_model=ProductResponse)
def delete_product(product_id: UUID):
    """
    Delete a product by its ID.

    Args:
        product_id (UUID): ID of the product to delete.

    Returns:
        ProductResponse: ProductResponse object of the deleted product.
    """

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger_api.error(f"Product with product id {product_id} does not exist.")
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} does not exist"
        )
    offers = session.query(Offer).filter(Offer.product_id == product_id).all()
    for offer in offers:
        session.delete(offer)
    session.delete(product)
    session.commit()
    logger_api.info(f"Deleted product with product id {product_id}.")
    return product
