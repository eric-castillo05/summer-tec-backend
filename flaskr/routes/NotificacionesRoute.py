from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskr.utils import Config
from flaskr.services.NotificacionesService import NotificacionesService

notificaciones_bp = Blueprint('notificaciones_bp', __name__)

notificacionesService = NotificacionesService()

@notificaciones_bp.route('/get-all/<string:usuario_id>', methods=['GET'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def get_notificaciones(usuario_id):
    current_user = get_jwt_identity()
    if current_user != usuario_id:
        return jsonify({"error": "No autorizado", "status": 403}), 403

    seen = request.args.get('seen', default=None, type=lambda v: v.lower() == 'true')
    result = notificacionesService.get_notificaciones(usuario_id, seen)
    return jsonify(result), result['status']

@notificaciones_bp.route('/create-notification', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def create_notificacion():
    data = request.get_json()
    data['creador_grupo_id'] = get_jwt_identity()
    result = notificacionesService.create_notificacion(data)
    return jsonify(result), result['status']


@notificaciones_bp.route('/update-seen/<int:id_notificacion>/seen', methods=['PUT'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def mark_as_seen(id_notificacion):
    current_user = get_jwt_identity()
    result = notificacionesService.mark_as_seen(id_notificacion, current_user)
    return jsonify(result), result['status']


@notificaciones_bp.route('/delete-notification/<int:id_notificacion>', methods=['DELETE'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
@jwt_required()
def delete_notificacion(id_notificacion):
    current_user = get_jwt_identity()
    result = notificacionesService.delete_notificacion(id_notificacion, current_user)
    return jsonify(result), result['status']