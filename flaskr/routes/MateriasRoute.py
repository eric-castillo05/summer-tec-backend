from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flaskr.utils import Config
from flaskr.services import MateriasService

materias_bp = Blueprint('materias_bp', __name__)

materiasService = MateriasService()

@materias_bp.route('/materias_all', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def materias_all():
    materias = materiasService.get_materias()
    return jsonify(materias), 200


@materias_bp.route('/materias_by_clave_carrera/<clave_carrera>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def materias_by_clave_carrera(clave_carrera):
    materias = materiasService.get_materias_by_clave_carrera(clave_carrera)

    if not materias:
        return jsonify({"message": "No materias found for the given clave_carrera"}), 404

    return jsonify(materias), 200

