import time
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from microservice.config.settings import Settings

JWT_SECRET = Settings.SECRET
JWT_ALGORITHM = Settings.ALGORITHM


def token_response(token: str):
    """
    Create a response containing an access token.

    Args:
        token (str): The JWT access token.

    Returns:
        dict: A dictionary containing the access token.
    """
    return {
        "access_token": token
    }


def sign_jwt(user_id: str):
    """
    Sign a JWT token.

    Args:
        user_id (str): The user ID to include in the token payload.

    Returns:
        dict: A dictionary containing the access token.
    """
    payload = {
        "userID": user_id,
        "expiry": int(time.time()) + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    """
    Decode a JWT token and check if it's valid.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict or None: The decoded token if valid and not expired, otherwise None.
    """
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decode_token['expiry'] >= int(time.time()):
            return decode_token
        else:
            return None
    except ExpiredSignatureError:
        return None
    except DecodeError:
        return None
