from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flaskr.services import AuthService
from flaskr.utils.config import Config

auth_bp = Blueprint('auth_bp', __name__)
auth_service = AuthService()

@auth_bp.route('/signup', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
def signup():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    required_fields = ['numero_control', 'nombre_completo', 'email', 'password', 'phone_number', 'clave_carrera']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    numero_control = data['numero_control']
    nombre_completo = data['nombre_completo']
    email = data['email']
    password = data['password']
    phone_number = data['phone_number']
    clave_carrera = data['clave_carrera']

    if '@' not in email:
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    result, status = auth_service.signup(numero_control, nombre_completo, email, password, phone_number, clave_carrera)
    return jsonify(result), status


@auth_bp.route('/login', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
def login():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    email = data['email']
    password = data['password']

    result, status = auth_service.login(email, password)
    return jsonify(result), status
