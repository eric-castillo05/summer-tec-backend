from flask import Blueprint, jsonify, request
from flaskr.services.MateriasPropuestasService import MateriasPropuestasService

materias_propuestas_bp = Blueprint("materias_propuestas_bp", __name__)

materiasPropuestasService = MateriasPropuestasService()

@materias_propuestas_bp.route("/materias_propuestas", methods=["GET"])
def get_materias():
    materias = materiasPropuestasService.get_materias_propuestas()
    return jsonify(materias)

@materias_propuestas_bp.route("/create_materia_propuesta", methods=["POST"])
def create_materia_propuesta():
    data = request.get_json()

    required_fields = ["materia_id", "clave_carrera", "status", "cupo", "turno"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not data.get("id_estudiante") and not data.get("id_coordinador"):
        return jsonify({"error": "Either 'id_estudiante' or 'id_coordinador' is required"}), 400

    if data.get("id_estudiante") and data.get("id_coordinador"):
        return jsonify({"error": "Only one of 'id_estudiante' or 'id_coordinador' should be provided"}), 400

    response = materiasPropuestasService.register_materia_propuesta(data)
    return jsonify(response), response.get("status", 201)