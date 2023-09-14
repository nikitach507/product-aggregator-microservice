from microservice.utils.logging_configure import get_logger

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from microservice.auth.jwt_handler import decode_jwt

logger_api = get_logger()


class JwtBearer(HTTPBearer):
    """
    Custom JWT Bearer Authentication for FastAPI.

    Args:
        auto_error (bool, optional): If True, automatically raise HTTPException on authentication errors. Defaults to True.
    """

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Authenticate the request based on the Bearer token.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            str: The Bearer token if authentication is successful.

        Raises:
            HTTPException: If authentication fails.
        """
        try:
            credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=401, detail="Invalid or Expired Token")
                return credentials.credentials
            else:
                raise HTTPException(status_code=401, detail="Invalid or Expired Token")
        except Exception as e:
            logger_api.error(f"Authentication error: {e}")
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Authentication Error")

    def verify_jwt(self, jwtoken: str):
        """
        Verify the authenticity of a JWT token.

        Args:
            jwtoken (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            is_token_valid: bool = False
            payload = decode_jwt(jwtoken)
            if payload:
                is_token_valid = True
            return is_token_valid
        except Exception as e:
            logger_api.error(f"JWT verification error: {e}")
            return False
