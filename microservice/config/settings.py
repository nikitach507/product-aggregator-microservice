from decouple import config


class Settings:
    SECRET = config("SECRET")
    ALGORITHM = config("ALGORITHM")

    BASE_URL = config("OFFER_HOST")
    PRODUCTS_REGISTER_ENDPOINT = config("PRODUCTS_REGISTER_ENDPOINT")
    AUTH_ENDPOINT = config("AUTH_ENDPOINT")
    DB_USERNAME = config("DB_USERNAME")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_NAME = config("DB_NAME")

    REFRESH_TOKEN = config("REFRESH_TOKEN")


