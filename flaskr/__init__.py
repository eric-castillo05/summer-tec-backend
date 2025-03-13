from flask import Flask

from flaskr.routes.AuthRoutes import auth_bp
from flaskr.routes.MateriasPropuestasRoutes import materias_propuestas_bp
from flaskr.utils.JWT import JWTManager
from flaskr.utils.db import Database


def create_app():
    app = Flask(__name__)

    Database().init_app(app)

    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')

    return app

