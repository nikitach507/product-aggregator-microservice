from fastapi import APIRouter, HTTPException, Query
from microservice.utils.logging_configure import get_logger
from pydantic import BaseModel
from microservice.models.models import Offer, Product
from microservice.database.database_setup import session
from uuid import UUID
from datetime import datetime
from scipy.stats import linregress

router = APIRouter()

logger_api = get_logger()


class OfferResponse(BaseModel):
    id: UUID
    price: int
    items_in_stock: int
    product_id: UUID


@router.get("/", response_model=list[OfferResponse])
def get_all_offers(skip: int = 0, limit: int = 100):
    """
    Get a list of all offers.

    Args:
        skip (int): Number of items to skip.
        limit (int): Maximum number of items to return.

    Returns:
        list[OfferResponse]: List of OfferResponse objects.
    """
    try:
        offers = session.query(Offer).offset(skip).limit(limit).all()

        # Convert SQLAlchemy objects to dictionaries
        offers_dict = [{"id": offer.id,
                        "price": offer.price,
                        "items_in_stock": offer.items_in_stock,
                        "product_id": str(offer.product_id)} for offer in offers]
        logger_api.info("Retrieved all offers successfully.")
        return offers_dict
    except Exception as exc:
        logger_api.exception(f"Error getting offers:")
        raise HTTPException(status_code=500, detail="Error getting offers")


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer_by_id(offer_id: UUID):
    """
    Get an offer by its ID.

    Args:
        offer_id (UUID): ID of the offer to retrieve.

    Returns:
        OfferResponse: OfferResponse object.
    """
    offer_by_id = session.query(Offer).filter(Offer.id == offer_id).first()
    if not offer_by_id:
        logger_api.error(f"Offer with offer id {offer_id} does not exist.")
        raise HTTPException(status_code=404, detail=f"Offer with id {offer_id} does not exist")
    logger_api.info(f"Retrieved product with offer id {offer_id}.")
    return offer_by_id


@router.get("/products/{product_id}", response_model=list[OfferResponse])
def get_offers_by_product_id(product_id: UUID):
    """
    Get offers by product ID.

    Args:
        product_id (UUID): ID of the product to retrieve offers for.

    Returns:
        list[OfferResponse]: List of OfferResponse objects for the specified product.
    """
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger_api.error(f"Product with product id {product_id} does not exist.")
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} does not exist")

    offers = session.query(Offer).filter(Offer.product_id == product_id).all()

    offers_dict = [{"id": offer.id,
                    "price": offer.price,
                    "items_in_stock": offer.items_in_stock,
                    "product_id": str(offer.product_id)} for offer in offers]
    logger_api.info(f"Retrieved all offers with product id {product_id}.")
    return offers_dict


@router.get("/price_trend/")
async def get_price_trend(
        product_id: str = Query(..., description="Product ID"),
        start_date: datetime = Query(..., description="Start date for the analysis"),
        end_date: datetime = Query(..., description="End date for the analysis")
):
    """
       Get the price trend and percentual rise/fall for a specified product within a given date range.

       Args:
           product_id (str): The ID of the product for analysis.
           start_date (datetime): The start date for the analysis.
           end_date (datetime): The end date for the analysis.

       Returns:
           dict: A dictionary containing the price trend, percent change, timestamps, and prices.
       """
    try:
        price_data = (
            session.query(Offer.timestamp, Offer.price)
            .filter(
                Offer.product_id == product_id,
                Offer.timestamp >= start_date,
                Offer.timestamp <= end_date
            )
            .order_by(Offer.timestamp)
            .all()
        )
        if not price_data:
            logger_api.info(f"No price data available for the specified period.")
            return {"message": "No price data available for the specified period."}

        timestamps, prices = zip(*price_data)

        slope, _, _, _, _ = linregress(range(len(prices)), prices)

        initial_price = prices[0]
        final_price = prices[-1]
        percent_change = ((final_price - initial_price) / initial_price) * 100

        logger_api.info(f"Successfully tracked the price.")
        return {
            "trend": slope,
            "percent_change": percent_change,
            "timestamps": timestamps,
            "prices": prices
        }
    except Exception as exc:
        logger_api.exception(f"Error getting price trend:")
        raise HTTPException(status_code=500, detail="Error getting price trend")
