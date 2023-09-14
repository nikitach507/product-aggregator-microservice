import threading
import time
import requests
from microservice.config.settings import Settings

from microservice.utils.logging_configure import get_logger

logger_api = get_logger()


class TokenManager:
    def __init__(self):
        self.access_token = None
        self.token_timestamp = 0
        self.token_lock = threading.Lock()

    def get_access_token(self):
        """
        Get an access token. If a valid token exists and is not expired, it will be returned.
        Otherwise, a new token will be obtained and returned.

        Returns:
            str or False: The access token if successful, False if an error occurs.
        """
        if self.access_token and (time.time() - self.token_timestamp < 300):
            logger_api.info(
                f"Using existing token, current token age: {time.time() - self.token_timestamp} seconds, max 300 seconds"
            )
            return self.access_token

        with self.token_lock:
            if not self.access_token or (time.time() - self.token_timestamp >= 300):
                self.access_token = self.update_access_token()
                self.token_timestamp = time.time()

                logger_api.info(f"Obtained a new access_token: {self.access_token}")
            return self.access_token

    @staticmethod
    def update_access_token():
        """
        Update the access token by making a request to the authentication API.

        Returns:
            str or False: The new access token if successful, False if an error occurs.
        """
        offer_service_url = f"{Settings.BASE_URL}{Settings.AUTH_ENDPOINT}"

        headers = {"Bearer": f"{Settings.REFRESH_TOKEN}"}

        response = requests.post(offer_service_url, timeout=10, headers=headers)

        if response.status_code == 201:
            response_json = response.json()
            new_access_token = response_json.get("access_token")
            return new_access_token

        raise Exception("No refresh token")


token_manager = TokenManager()
