from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from flaskr.utils import Config
from flaskr.services.DocenteService import DocenteService

docentes_bp = Blueprint('docentes_bp', __name__)

docentesService = DocenteService()

@docentes_bp.route('/get_by_clave/<clave_carrera>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_by_clave(clave_carrera):
    docentes = docentesService.get_all(clave_carrera=clave_carrera)
    return jsonify(docentes), 200