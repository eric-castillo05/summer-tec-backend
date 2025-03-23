from flask import Blueprint, request, jsonify
import time
import requests
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
import logging

from flaskr.services import AuthService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

registry = CollectorRegistry()

login_counter = Counter('flask_login_total', 'Total number of login attempts',
                        ['status'], registry=registry)
signup_counter = Counter('flask_signup_total', 'Total number of signup attempts',
                         ['status'], registry=registry)
request_latency = Histogram('flask_request_latency_seconds', 'Request latency in seconds',
                            ['endpoint'], registry=registry)

GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin"
GRAFANA_PUSH_URL = "http://pushgateway:9091/metrics/job/flask_app"

auth_bp = Blueprint('auth_bp', __name__)

auth_service = AuthService()

def push_to_grafana_local():
    try:
        headers = {
            'Content-Type': 'text/plain',
        }
        # No need for cloud credentials here
        data = generate_latest(registry)
        response = requests.post(
            GRAFANA_PUSH_URL,
            headers=headers,
            data=data
        )
        if response.status_code >= 400:
            logger.error(f"Error pushing metrics to local Grafana: {response.status_code} {response.text}")
        else:
            logger.info("Successfully pushed metrics to local Grafana")
    except Exception as e:
        logger.error(f"Exception while pushing metrics: {e}")


@auth_bp.route('/signup', methods=['POST'])
def signup():
    start_time = time.time()

    data = request.get_json()
    required_fields = ['numero_control', 'nombre_completo', 'email', 'password', 'phone_number']
    if not all(field in data for field in required_fields):
        signup_counter.labels(status="failed").inc()
        try:
            push_to_grafana_local()
        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")
        return jsonify({"error": "Missing required fields"}), 400

    numero_control = data['numero_control']
    nombre_completo = data['nombre_completo']
    email = data['email']
    password = data['password']
    phone_number = data['phone_number']

    if '@' not in email:
        signup_counter.labels(status="failed").inc()
        try:
            push_to_grafana_local()
        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8:
        signup_counter.labels(status="failed").inc()
        try:
            push_to_grafana_local()
        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    result, status = auth_service.signup(numero_control, nombre_completo, email, password, phone_number)

    signup_counter.labels(status="success" if status == 201 else "failed").inc()
    request_latency.labels(endpoint="/signup").observe(time.time() - start_time)

    try:
        push_to_grafana_local()
    except Exception as e:
        logger.error(f"Failed to push metrics: {e}")

    return jsonify(result), status


@auth_bp.route('/login', methods=['POST'])
def login():
    start_time = time.time()

    data = request.get_json()
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        login_counter.labels(status="failed").inc()
        try:
            push_to_grafana_local()
        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")
        return jsonify({"error": "Missing required fields"}), 400

    email = data['email']
    password = data['password']

    result, status = auth_service.login(email, password)

    login_counter.labels(status="success" if status == 200 else "failed").inc()
    request_latency.labels(endpoint="/login").observe(time.time() - start_time)

    try:
        push_to_grafana_local()
    except Exception as e:
        logger.error(f"Failed to push metrics: {e}")

    return jsonify(result), status



@auth_bp.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()