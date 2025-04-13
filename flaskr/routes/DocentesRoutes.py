import uuid

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from flaskr.models import Docente
from flaskr.utils import Config
from flaskr.utils.db import db
from flaskr.services.DocenteService import DocenteService

docentes_bp = Blueprint('docentes_bp', __name__)

docentesService = DocenteService()

@docentes_bp.route('/get_by_clave/<clave_carrera>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_by_clave(clave_carrera):
    docentes = docentesService.get_all(clave_carrera=clave_carrera)
    return jsonify(docentes), 200

@docentes_bp.route('/create_docente', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def create_docente():
    data = request.get_json()
    result = docentesService.create_docente(data)

    if "error" in result:
        return jsonify({"error": result["error"]}), result["status"]

    return jsonify({
        "message": result["message"],
        "docente": result["docente"]
    }), result["status"]