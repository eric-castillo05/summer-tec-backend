from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt
from flaskr.utils import Config
from flaskr.services.MateriasPropuestasService import MateriasPropuestasService

materias_propuestas_bp = Blueprint("materias_propuestas_bp", __name__)

materiasPropuestasService = MateriasPropuestasService()


@materias_propuestas_bp.route("/materias_propuestas", methods=["GET"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_materias():
    claims = get_jwt()

    if not claims.get("role") == "ADMIN":
        return jsonify({"error": "Unauthorized. Only administrators can access this resource."}), 403

    materias = materiasPropuestasService.get_materias_propuestas()
    return jsonify(materias)


@materias_propuestas_bp.route("/create_materia_propuesta", methods=["POST"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def create_materia_propuesta():
    data = request.get_json()

    required_fields = ["materia_id", "clave_carrera", "status", "turno"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Check that at least one creator is provided
    if not any(key in data for key in ["id_estudiante", "id_coordinador", "id_admin"]):
        return jsonify({"error": "At least one of 'id_estudiante', 'id_coordinador', or 'id_admin' is required"}), 400

    # Check that only one creator is provided
    creators = [key for key in ["id_estudiante", "id_coordinador", "id_admin"] if key in data]
    if len(creators) > 1:
        return jsonify(
            {"error": "Only one of 'id_estudiante', 'id_coordinador', or 'id_admin' should be provided"}), 400

    response = materiasPropuestasService.register_materia_propuesta(data)

    # Extract status from response or default to 201
    status_code = response.pop("status", 201) if isinstance(response, dict) else 201

    return jsonify(response), status_code