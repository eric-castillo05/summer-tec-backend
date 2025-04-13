from flask import Flask
from flask_cors import CORS
from flaskr.routes.AuthRoutes import auth_bp
from flaskr.routes.EstudinteRoutes import estudiante_bp
from flaskr.routes.MateriasPropuestasRoutes import materias_propuestas_bp
from flaskr.routes.MateriasRoute import materias_bp
from flaskr.utils.JWT import JWT
from flaskr.utils.config import Config
from flaskr.utils.db import Database


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": Config.ROUTE}}, supports_credentials=True)

    Database().init_app(app)

    jwt = JWT(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')
    app.register_blueprint(materias_bp, url_prefix='/materias')
    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')


    return app