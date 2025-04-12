import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask_cors import CORS
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.semconv.attributes.service_attributes import SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from flaskr.routes.AuthRoutes import auth_bp
from flaskr.routes.MateriasPropuestasRoutes import materias_propuestas_bp
import os

from flaskr.routes.MateriasRoute import materias_bp
from flaskr.utils.JWT import JWT
from flaskr.utils.config import Config
from flaskr.utils.db import Database
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": Config.ROUTE}}, supports_credentials=True)

    Database().init_app(app)

    jwt = JWT(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')
    app.register_blueprint(materias_bp, url_prefix='/materias')


    return app