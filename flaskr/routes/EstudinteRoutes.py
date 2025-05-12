from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from flaskr.utils import Config
from flaskr.services import EstudianteService

estudiante_bp = Blueprint('estudiante', __name__, url_prefix='/estudiante')

estudianteService = EstudianteService()


@estudiante_bp.route('/inscribir/', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def inscribir():
    data = request.get_json()
    estudiante_id = data['estudiante_id']
    materia_propuesta_id = data['materia_propuesta_id']

    response = estudianteService.inscribir_estudiante(estudiante_id, materia_propuesta_id)
    status_code = response.pop("status", 200) if isinstance(response, dict) else 200

    return jsonify(response), status_code


@estudiante_bp.route('/baja/', methods=['DELETE'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def baja():
    data = request.get_json()
    estudiante_id = data['estudiante_id']
    materia_propuesta_id = data['materia_propuesta_id']

    response = estudianteService.baja_estudiante(estudiante_id, materia_propuesta_id)
    status_code = response.pop("status", 200) if isinstance(response, dict) else 200

    return jsonify(response), status_code


@estudiante_bp.route('/inscritos/<int:materia_propuesta_id>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def obtener_inscritos(materia_propuesta_id):
    estudiantes = estudianteService.obtener_estudiantes_inscritos(materia_propuesta_id)
    return jsonify(estudiantes), 200


@estudiante_bp.route('/mis-grupos', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def obtener_mis_grupos():
    # Intentar obtener el estudiante_id del encabezado
    estudiante_id = request.headers.get('estudiante_id')

    # Si no está en el encabezado, intentar obtenerlo de los parámetros de la URL
    if not estudiante_id:
        estudiante_id = request.args.get('estudiante_id')

    # Si todavía no lo tenemos, intentar obtenerlo del cuerpo JSON (aunque no debería ser necesario para GET)
    if not estudiante_id and request.is_json:
        try:
            data = request.get_json()
            estudiante_id = data.get('estudiante_id')
        except:
            pass

    # Si no se encontró el ID del estudiante, devolver un error
    if not estudiante_id:
        return jsonify({"error": "No se proporcionó el ID del estudiante"}), 400

    response = estudianteService.obtener_mis_grupos(estudiante_id)

    # Extraer el código de estado si existe
    status_code = response.pop("status", 200) if isinstance(response, dict) else 200

    # Si hay un campo "grupos" en la respuesta, devolver solo ese campo
    if isinstance(response, dict) and "grupos" in response:
        return jsonify(response["grupos"]), status_code

    return jsonify(response), status_code