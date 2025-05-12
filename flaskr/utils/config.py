import os

from flask.cli import load_dotenv

load_dotenv()
class Config:
    USER_DB = os.getenv("USER_DB")
    PASSWORD_DB = os.getenv("PASSWORD_DB")
    HOST_DB = os.getenv("HOST_DB")
    PORT_DB = os.getenv("PORT_DB")
    BD_NAME = os.getenv("BD_NAME")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ROUTE = os.getenv("ROUTE")
    ADMIN_USER = os.getenv("ADMIN_USER")
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
