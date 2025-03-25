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
from flaskr.utils.JWT import JWT
from flaskr.utils.db import Database
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "https://summertec.onrender.com"}}, supports_credentials=True)

    # OpenTelemetry Tracing Setup
    resource = Resource.create({SERVICE_NAME: "flaskr"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces")
    span_processor = SimpleSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    FlaskInstrumentor().instrument_app(app)

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "flask.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(stream_handler)

    logger.info("Flask app started - logging initialized")

    @app.before_request
    def add_start_time():
        request.start_time = time.time()

    @app.after_request
    def log_request(response):
        response_time = (time.time() - request.start_time) * 1000 if hasattr(request, 'start_time') else 0
        logger.info(
            f"Request to {request.path} method={request.method} "
            f"completed with status={response.status_code} "
            f"response_time={response_time:.2f}ms"
        )
        return response

    Database().init_app(app)

    jwt = JWT(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    return app