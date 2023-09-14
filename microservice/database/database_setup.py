from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from microservice.config.settings import Settings


engine = create_engine(
    f"postgresql://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}/{Settings.DB_NAME}"
)

Session = sessionmaker(bind=engine)
session = Session()
