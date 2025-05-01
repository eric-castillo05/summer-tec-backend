from datetime import datetime

from flaskr.models import Notificaciones, NotificacionesEnum, Usuarios, RolesEnum
from flaskr.utils.db import db

class NotificacionesService:
    def __init__(self):
        pass

    def create_notificacion(self, data):
        tipo = data.get('tipo')
        creador_grupo_id = data.get('creador_grupo_id')
        usuario_id = data.get('usuario_id')
        tipo_usuario = data.get('tipo_usuario')
        materia_propuesta_id = data.get('materia_propuesta_id')

        if not tipo or tipo not in NotificacionesEnum.__members__:
            return {"error": "Tipo de notificación inválido", "status": 400}
        if not creador_grupo_id or not Usuarios.query.get(creador_grupo_id):
            return {"error": "Creador del grupo no encontrado", "status": 404}
        if not usuario_id or not Usuarios.query.get(usuario_id):
            return {"error": "Usuario receptor no encontrado", "status": 404}
        if not tipo_usuario or tipo_usuario not in RolesEnum.__members__:
            return {"error": "Tipo de usuario inválido", "status": 400}

        notificacion = Notificaciones(
            tipo=NotificacionesEnum[tipo],
            creador_grupo_id=creador_grupo_id,
            usuario_id=usuario_id,
            tipo_usuario=RolesEnum[tipo_usuario],
            materia_propuesta_id=materia_propuesta_id,
            seen=False,
            fecha_creacion=datetime.now()
        )

        db.session.add(notificacion)
        db.session.commit()
        return {'message': 'Notificacion creada correctamente', 'status': 200}


    def get_notificaciones(self, usuario_id):
        if not Usuarios.query.get(usuario_id):
            return {"error": "Usuario no encontrado", "status": 404}

        query = Notificaciones.query.filter_by(usuario_id=usuario_id, seen=False)
        notificaciones = query.all()

        if not notificaciones:
            return {"message": "No hay notificaciones", "notificaciones": [], "status": 404}

        result = [
            {
                "id_notificacion": n.id_notificacion,
                "tipo": n.tipo.value,
                "creador_grupo": n.creador.nombre_completo,
                "hora": n.fecha_creacion.isoformat(),
                "usuario_id": n.usuario_id,
                "tipo_usuario": n.tipo_usuario.value,
                "seen": n.seen,
                "materia_propuesta_id": n.materia_propuesta_id
            }
            for n in notificaciones
        ]

        return {"notificaciones": result, "status": 200}


    def get_notificaciones_all(self, usuario_id):
        if not Usuarios.query.get(usuario_id):
            return {"error": "Usuario no encontrado", "status": 404}

        notificaciones = Notificaciones.query.all()

        if not notificaciones:
            return {"message": "No hay notificaciones", "notificaciones": [], "status": 404}

        result = [
            {
                "id_notificacion": n.id_notificacion,
                "tipo": n.tipo.value,
                "creador_grupo": n.creador.nombre_completo,
                "hora": n.fecha_creacion.isoformat(),
                "usuario_id": n.usuario_id,
                "tipo_usuario": n.tipo_usuario.value,
                "seen": n.seen,
                "materia_propuesta_id": n.materia_propuesta_id
            }
            for n in notificaciones
        ]

        return {"notificaciones": result, "status": 200}

    def mark_as_seen(self, id_notificacion, usuario_id):
        try:
            notificacion = Notificaciones.query.get(id_notificacion)
            if not notificacion:
                return {"error": "Notificación no encontrada", "status": 404}
            if notificacion.usuario_id != usuario_id:
                return {"error": "No autorizado", "status": 403}

            notificacion.seen = True
            db.session.commit()

            return {"message": "Notificación marcada como vista", "status": 200}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Error al marcar notificación: {str(e)}", "status": 500}

    def delete_notificacion(self, id_notificacion, usuario_id):
        try:
            notificacion = Notificaciones.query.get(id_notificacion)
            if not notificacion:
                return {"error": "Notificación no encontrada", "status": 404}
            if notificacion.usuario_id != usuario_id:
                return {"error": "No autorizado", "status": 403}

            db.session.delete(notificacion)
            db.session.commit()

            return {"message": "Notificación eliminada correctamente", "status": 200}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Error al eliminar notificación: {str(e)}", "status": 500}