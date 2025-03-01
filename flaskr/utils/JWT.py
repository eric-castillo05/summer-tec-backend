from threading import Lock

from flask_jwt_extended import JWTManager

from flaskr.utils.config import Config


class JWT:
    _instance = None
    _lock = Lock()

    def __new__(cls, app = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(JWT, cls).__new__(cls)
                    cls._instance.jwt = JWTManager()
                    if app is not None:
                        cls._instance.init_app(app)
        return cls._instance

    def init_app(self, app):
        app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
        self.jwt.init_app(app)