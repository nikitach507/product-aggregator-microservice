import threading
import time
from microservice.utils.logging_configure import get_logger

from microservice.services.offers import get_product_offer_data
from microservice.services.token_manager import token_manager
from microservice.database.database_setup import session
from microservice.models.models import Offer, Product

logger_background = get_logger()


class BackgroundService:
    """
    A background service for updating offers data periodically.
    """

    def __init__(self):
        """
        Initialize the BackgroundService instance.
        """
        self.access_token: str = None
        self.token_timestamp: float = 0
        self.running = True

    def update_offers_data(self):
        """
        Update offers data from the offers microservice.

        This method retrieves access tokens, queries product data, and updates offers in the database.
        """
        if time.time() - self.token_timestamp >= 300:
            self.access_token = None
        logger_background.info("The process of updating the proposals has begun.")
        if not self.access_token:
            try:
                self.access_token = token_manager.get_access_token()
                self.token_timestamp = time.time()
            except Exception as exc:
                logger_background.exception("No token provided, retrying...")
                return
        products = session.query(Product).all()

        for product in products:
            try:
                offer_data = get_product_offer_data(
                    self.access_token, product.id
                )

                session.query(Offer).filter(Offer.product_id == product.id).delete()
                session.commit()

                for offer in offer_data:
                    offer_db = Offer(
                        id=offer["id"],
                        price=offer["price"],
                        items_in_stock=offer["items_in_stock"],
                        product_id=product.id,
                    )
                    session.add(offer_db)
                    session.commit()
            except Exception as exc:
                logger_background.exception(
                    "Error processing product id %s", product.id,
                )

            logger_background.info("Updated offers for the product ID: %s", product.id)
        logger_background.info("The process of updating the proposals has ended.")

    def run_periodically(self):
        """
        Run periodically the update_offers_data method.

        This method starts the background service and schedules the update_offers_data method to run every 3 minutes.
        """
        logger_background.info("Background service started.")
        interval_minutes = 1

        def periodic_task():
            while self.running:
                try:
                    self.update_offers_data()
                    time.sleep(interval_minutes * 60)
                except Exception as exc:
                    logger_background.exception("An error occurred:")

        periodic_thread = threading.Thread(target=periodic_task)
        periodic_thread.daemon = True
        periodic_thread.start()

    def stop(self):
        self.running = False
