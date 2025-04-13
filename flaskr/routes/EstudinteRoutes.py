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


