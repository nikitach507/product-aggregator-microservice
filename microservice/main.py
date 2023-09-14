from logging.config import dictConfig
from threading import Thread

from fastapi import FastAPI

from microservice.background_service.background_service import \
    BackgroundService
from microservice.database.database_setup import engine
from microservice.models.base_model import Base
from microservice.models.auth_model import User
from microservice.models.models import Offer, Product
from microservice.routes.api import api_router
from microservice.utils.logging_configure import LogConfig

app = FastAPI()
app.include_router(api_router)

dictConfig(LogConfig().model_dump())

bg_service = BackgroundService()

Base.metadata.create_all(engine)


@app.on_event("startup")
def startup():
    thread = Thread(target=bg_service.run_periodically)
    thread.start()


@app.on_event("shutdown")
def shutdown():
    bg_service.stop()