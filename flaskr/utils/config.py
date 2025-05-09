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
