from threading import Lock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database
from flaskr.utils.config import Config

db = SQLAlchemy()

class Database:
    _instance = None
    _lock = Lock()


    def __new__(cls, app = None):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db = db
                if app:
                    cls._instance.init_app(app)
        return cls._instance



    def init_app(self, app):
        if hasattr(self, 'initialized') and self.initialized:
            return
        db_uri = f'mysql+pymysql://{Config.USER_DB}:{Config.PASSWORD_DB}@{Config.HOST_DB}:{Config.PORT_DB}/{Config.BD_NAME}'
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        engine = create_engine(db_uri)
        if not database_exists(engine.url):
            create_database(engine.url)

        db.init_app(app)
        self.initialized = True