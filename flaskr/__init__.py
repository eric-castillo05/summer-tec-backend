import logging
from flask import Flask
from flaskr.routes.AuthRoutes import auth_bp
from flaskr.routes.MateriasPropuestasRoutes import materias_propuestas_bp
from flaskr.utils import JsonFormatter
from flaskr.utils.JWT import JWT
from flaskr.utils.db import Database
from flask_prometheus_metrics import register_metrics
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


def create_app():
    app = Flask(__name__)

    Database().init_app(app)

    jwt = JWT(app)


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })


    return app

