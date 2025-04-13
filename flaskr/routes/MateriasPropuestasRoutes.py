from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt

from flaskr.models import Horario
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


@materias_propuestas_bp.route("/update_materias_propuestas/<int:id_materia_propuesta>", methods=["PUT"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def update_materia_propuesta(id_materia_propuesta):
    claims = get_jwt()
    if claims.get("role") not in ["COORDINADOR", "ADMIN"]:
        return jsonify({"error": "No autorizado. Solo coordinadores o administradores pueden modificar."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos para actualizar"}), 400

    response = materiasPropuestasService.update_materia_propuesta(id_materia_propuesta, data)
    status_code = response.pop("status", 200) if isinstance(response, dict) else 200

    return jsonify(response), status_code


@materias_propuestas_bp.route("/delete_materias_propuestas/<int:id_materia_propuesta>", methods=["DELETE"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def delete_materia_propuesta(id_materia_propuesta):
    claims = get_jwt()
    if claims.get("role") not in ["COORDINADOR", "ADMIN"]:
        return jsonify({"error": "No autorizado. Solo coordinadores o administradores pueden eliminar."}), 403

    response = materiasPropuestasService.delete_materia_propuesta(id_materia_propuesta)
    status_code = response.pop("status", 200) if isinstance(response, dict) else 200

    return jsonify(response), status_code


@materias_propuestas_bp.route("/get_by_status_carrera/<status>/<clave_carrera>", methods=["GET"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_materias_by_status_and_carrera(status, clave_carrera):
    materias = materiasPropuestasService.get_by_status_and_carrera(status, clave_carrera)
    return jsonify(materias), 200


@materias_propuestas_bp.route("/get_all_by_status/status/<status>", methods=["GET"])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_materias_by_status(status):
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({"error": "Unauthorized. Only administrators can access this resource."}), 403
    materias = materiasPropuestasService.get_by_status(status)
    return jsonify(materias), 200


@materias_propuestas_bp.route('/horarios-por-edificio/<id_edificio>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def obtener_horarios_por_edificio(id_edificio):
    horarios = Horario.query.filter_by(edificio_id=id_edificio).all()

    resultado = []
    for horario in horarios:
        materia = horario.materia_propuesta.materia if horario.materia_propuesta else None
        resultado.append({
            'id_horario': horario.id_horario,
            'materia_propuesta_id': horario.materia_propuesta_id,
            'nombre_materia': materia.nombre_materia if materia else None,
            'dia': horario.dia_semana.name,
            'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
            'hora_fin': horario.hora_fin.strftime('%H:%M'),
            'aula_id': horario.aula_id,
            'edificio_id': horario.edificio_id
        })

    return jsonify({
        'edificio': id_edificio,
        'horarios': resultado
    })