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

    required_fields = ['nombre_completo', 'clave_carrera', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    new_docente = Docente(
        id_docente=str(uuid.uuid4()),
        nombre_completo=data['nombre_completo'],
        clave_carrera=data['clave_carrera'],
        email=data['email']
    )

    db.session.add(new_docente)
    db.session.commit()

    return jsonify({
        "message": "Docente creado exitosamente",
        "docente": {
            "id_docente": new_docente.id_docente,
            "nombre_completo": new_docente.nombre_completo,
            "clave_carrera": new_docente.clave_carrera,
            "email": new_docente.email
        }
    }), 201