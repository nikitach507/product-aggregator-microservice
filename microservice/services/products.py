import requests
from microservice.utils.logging_configure import get_logger
from microservice.config.settings import Settings

logger_api = get_logger()


def register_product_in_offer_service(access_token: str, product_info: dict):
    """
    Register a product in the offer service using the provided access token and product information.

    Args:
        access_token (str): The access token for authentication.
        product_info (dict): The product information to register.

    Returns:
        bool: True if the registration is successful, False otherwise.
    """
    offer_service_url = f"{Settings.BASE_URL}{Settings.PRODUCTS_REGISTER_ENDPOINT}"
    try:
        headers = {
            "Bearer": access_token
        }

        response = requests.post(offer_service_url, json=product_info, headers=headers)

        if response.status_code == 201:
            logger_api.info("Product registration successful.")
            return True
        else:
            logger_api.error(f"API Error - Status Code: {response.status_code}")
            logger_api.error(f"API Response Content: {response.content.decode('utf-8')}")
            return False

    except Exception as exc:
        logger_api.exception(f"Exception:")
        return False

