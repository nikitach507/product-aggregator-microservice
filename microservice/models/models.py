import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from microservice.models.base_model import Base


class Product(Base):
    """
    Represents a product in the database.

    Attributes:
        id (UUID): The unique identifier for the product.
        name (str): The name of the product.
        description (str): The description of the product.
    """

    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String)
    description = Column(String)

    offers = relationship("Offer", back_populates="product")


class Offer(Base):
    """
    Represents an offer for a product in the database.

    Attributes:
        id (UUID): The unique identifier for the offer.
        price (int): The price of the offer.
        items_in_stock (int): The number of items in stock for the offer.
        product_id (UUID): The foreign key referencing the associated product.
    """

    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    price = Column(Integer)
    items_in_stock = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    product = relationship("Product", back_populates="offers")


