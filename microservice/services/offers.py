import requests
from microservice.utils.logging_configure import get_logger
from microservice.config.settings import Settings


logger_api = get_logger()


def get_product_offer_data(access_token, product_id):
    """
    Get offer data for a product using the provided access token and product ID.

    Args:
        access_token (str): The access token for authentication.
        product_id (str): The ID of the product for which to retrieve offer data.

    Returns:
        dict or bool: A dictionary containing offer data if successful, False otherwise.
    """
    offer_service_url = f"{Settings.BASE_URL}/api/v1/products/{product_id}/offers"

    headers = {
        "Bearer": access_token
    }

    try:
        response = requests.get(offer_service_url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            logger_api.error(f"API Error - Status Code: {response.status_code}")
            logger_api.error(f"API Response Content: {response.content.decode('utf-8')}")
            return False

    except Exception as exc:
        logger_api.exception(f"Exception:")
        return False


