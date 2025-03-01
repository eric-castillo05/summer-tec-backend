from flask import Flask

from flaskr.routes.AuthRoutes import auth_bp
from flaskr.utils.JWT import JWT
from flaskr.utils.db import Database


def create_app():
    app = Flask(__name__)

    Database().init_app(app)

    jwt = JWT(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

