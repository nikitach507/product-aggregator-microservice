import re
from sqlalchemy import Column, String
import uuid
from sqlalchemy.dialects.postgresql import UUID
from passlib.hash import bcrypt_sha256
from microservice.utils.logging_configure import get_logger
from microservice.models.base_model import Base


logger_api = get_logger()


class User(Base):
    """
    SQLAlchemy model for user information.

    Attributes:
        id (UUID): Unique identifier for the user.
        username (str): User's username.
        email (str): User's email address.
        hashed_password (str): Hashed user password.

    """
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def set_password(self, password: str):
        """
        Set and hash the user's password.

        Args:
            password (str): User's plain text password.

        """
        try:
            self.hashed_password = bcrypt_sha256.hash(password)
        except Exception as e:
            logger_api.error(f"Error hashing password: {e}")

    def check_password(self, password: str):
        """
        Check if the provided password matches the hashed password.

        Args:
            password (str): User's plain text password.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        try:
            return bcrypt_sha256.verify(password, self.hashed_password)
        except Exception as e:
            logger_api.error(f"Error verifying password: {e}")
            return False


def is_valid_password(password: str):
    """
    Check if a password meets complexity requirements.

    Args:
        password (str): User's plain text password.

    Returns:
        bool: True if the password meets complexity requirements, False otherwise.
    """
    regex_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    try:
        return re.match(regex_pattern, password) is not None
    except Exception as e:
        logger_api.error(f"Error checking password complexity: {e}")
        return False
