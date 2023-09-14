from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Body
from microservice.utils.logging_configure import get_logger
from microservice.auth.jwt_handler import sign_jwt
from microservice.models.auth_model import User, is_valid_password
from microservice.database.database_setup import session

logger_api = get_logger()

router = APIRouter()


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


@router.post("/signup")
def user_signup(user: UserSchema = Body(default=None)):
    """
    Create a new user account.

    Args:
        user (UserSchema): User information including username, email, and password.

    Returns:
        str: JWT token if the user account is successfully created.

    Raises:
        Exception: If the provided password does not meet complexity requirements.
    """
    if not is_valid_password(user.password):
        logger_api.error("Password does not meet complexity requirements.")
        raise Exception("Password does not meet complexity requirements.")

    user_db = User(username=user.username, email=user.email)
    user_db.set_password(user.password)
    session.add(user_db)
    session.commit()
    logger_api.info(f"User with email {user.email} successfully added")
    return sign_jwt(user.email)


def check_user(data: UserLoginSchema):
    """
    Check if the user login credentials are valid.

    Args:
        data (UserLoginSchema): User login information including email and password.

    Returns:
        bool: True if the user login is valid, False otherwise.
    """
    user = session.query(User).filter_by(email=data.email).first()
    if user and user.check_password(data.password):
        return True
    return False


@router.post("/login")
def user_login(user: UserLoginSchema = Body(default=None)):
    """
    Authenticate a user and return a JWT token if the login is successful.

    Args:
        user (UserLoginSchema): User login information including email and password.

    Returns:
        Union[str, dict]: JWT token if login is successful, or an error message if login fails.
    """
    if check_user(user):
        logger_api.info(f"User with email {user.email} successfully logged in.")
        return sign_jwt(user.email)
    else:
        logger_api.error("Invalid login attempt for email: %s", user.email)
        return {"error": "Invalid login details!"}