from datetime import datetime, time
from sqlalchemy.orm import aliased
from flaskr.utils import Config
from flaskr.models import Docente, StatusEnum, TurnoEnum, RolesEnum, Horario, Edificios, Usuarios, Carreras, \
    Notificaciones, NotificacionesEnum
from flaskr.routes.NotificacionesRoute import notificacionesService
from flaskr.services import EstudianteService
from flaskr.utils.db import db
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models.materias import Materias
from flaskr.models.aulas import Aula
from flaskr.models.horario import DiaSemanaEnum


class MateriasPropuestasService:
    def __init__(self):
        self.estudiante_service = EstudianteService()

    def get_materias_propuestas(self):
        # Alias para la tabla User para referenciar diferentes tipos de usuarios
        usuario_alias = aliased(Usuarios)

        # Query para obtener las materias propuestas con las relaciones necesarias
        materias = (
            db.session.query(
                Materias.horas_semana,
                Materias.creditos,
                Materias_Propuestas.cupo,
                Materias_Propuestas.turno,
                Materias_Propuestas.id_materia_propuesta,
                Docente.nombre_completo.label("profesor"),
                Materias.nombre_materia,
                Materias.clave_materia,
                Materias.clave_carrera,
                usuario_alias.email.label("email"),
                usuario_alias.rol.label("role"),
                Aula.aula_id.label("aula"),
                Edificios.numero_edificio.label("edificio"),
                Materias_Propuestas.status
            )
            .join(Materias_Propuestas, Materias.clave_materia == Materias_Propuestas.materia_id)
            .join(Docente, Materias_Propuestas.docente == Docente.email, isouter=True)
            .join(usuario_alias, Materias_Propuestas.user_id == usuario_alias.email)
            .outerjoin(Horario, Materias_Propuestas.id_materia_propuesta == Horario.materia_propuesta_id)
            .outerjoin(Aula, Horario.aula_id == Aula.aula_id)
            .outerjoin(Edificios, Aula.edificio_id == Edificios.numero_edificio)
            .all()
        )

        return [
            {
                "horas_semana": materia.horas_semana,
                "creditos": materia.creditos,
                "cupo": materia.cupo,
                "turno": materia.turno.name if materia.turno else None,
                "id_materia": materia.id_materia_propuesta,
                "profesor": materia.profesor,
                "nombre_materia": materia.nombre_materia,
                "clave_materia": materia.clave_materia,
                "clave_carrera": materia.clave_carrera,
                "creado_por": materia.email,
                "aula": materia.aula,
                "edificio": materia.edificio,
                "status": materia.status.name if materia.status else None
            }
            for materia in materias
        ]


    def register_materia_propuesta(self, data):
        user_id = data.get("user_id")
        if not user_id:
            return {"error": "Se requiere un user_id válido", "status": 400}

        # Verificar que el usuario existe y obtener su rol
        usuario = db.session.query(Usuarios).filter_by(email=user_id).first()
        if not usuario:
            return {"error": "Usuario no encontrado", "status": 404}

        # Verificar límite de creación para estudiantes
        if usuario.rol == RolesEnum.ESTUDIANTE:
            result = self.estudiante_service.can_create_materia_propuesta(user_id)
            if not result.get("can_create", False):
                return {"error": result.get("message", "Se ha alcanzado el límite de propuestas"), "status": 400}


        try:
            new_materia = Materias_Propuestas(
                user_id=user_id,
                materia_id=data["materia_id"],
                clave_carrera=data["clave_carrera"],
                status=StatusEnum.PENDIENTE,
                turno=TurnoEnum[data["turno"]],
                fecha_creacion=datetime.now(),
                cupo=data.get("cupo", 25),
                docente=data.get("docente"),
            )

            db.session.add(new_materia)
            db.session.flush()

            data = {
                "tipo": NotificacionesEnum.NUEVO_GRUPO.name,
                "creador_grupo_id": user_id,
                "usuario_id": user_id,
                "tipo_usuario":usuario.rol.name,
                "materia_propuesta_id": new_materia.id_materia_propuesta
            }
            notifiaciones_result = notificacionesService.create_notificacion(data)
            if notifiaciones_result['status'] != 201:
                db.session.rollback()


            saved_horarios = []
            horarios = data.get("horario", [])
            for h in horarios:
                horario = Horario(
                    dia_semana=h["dia"],
                    hora_inicio=time.fromisoformat(h["inicio"]),
                    hora_fin=time.fromisoformat(h["fin"]),
                    aula_id=h["aula_id"],
                    edificio_id=h["edificio_id"],
                    materia_propuesta_id=new_materia.id_materia_propuesta
                )
                db.session.add(horario)
                saved_horarios.append(horario)

            db.session.commit()

            return {
                "message": "Materia propuesta registrada con éxito",
                "status": 201,
                "id_materia_propuesta": new_materia.id_materia_propuesta,
                "user_id": new_materia.user_id,
                "rol_usuario": usuario.rol.name,
                "horarios": [
                    {
                        "id_horario": h.id_horario,
                        "dia": h.dia_semana.name,
                        "inicio": h.hora_inicio.strftime("%H:%M"),
                        "fin": h.hora_fin.strftime("%H:%M"),
                        "aula_id": h.aula_id,
                        "edificio_id": h.edificio_id
                    }
                    for h in saved_horarios
                ]
            }

        except KeyError as e:
            return {"error": f"Clave inválida: {str(e)}", "status": 400}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Ha ocurrido un error: {str(e)}", "status": 500}

    def update_materia_propuesta(self, id_materia_propuesta, data):
        materia = Materias_Propuestas.query.get(id_materia_propuesta)
        id_usuario = Materias_Propuestas.query.get(id_materia_propuesta).user_id
        if not materia:
            return {"error": "Materia propuesta no encontrada", "status": 404}

        # Actualización de campos simples
        if "aula_id" in data:
            materia.aula_id = data["aula_id"]
        if "status" in data:
            materia.status = StatusEnum(data["status"])
        if "docente" in data:
            materia.docente = data["docente"]

        data_horario = {
            "tipo": NotificacionesEnum.GRUPO_ACTUALIZADO.name,
            "creador_grupo_id": data['user_id'],
            "usuario_id": id_usuario,
            "tipo_usuario": data['role'],
            "materia_propuesta_id": id_materia_propuesta
        }
        notifiaciones_result = notificacionesService.create_notificacion(data_horario)
        if notifiaciones_result['status'] != 201:
            db.session.rollback()

        # Actualizar horarios si se proporcionan
        if "horarios" in data:
            # Borrar horarios existentes
            Horario.query.filter_by(materia_propuesta_id=id_materia_propuesta).delete()

            # Crear nuevos horarios
            for h in data["horarios"]:
                nuevo_horario = Horario(
                    materia_propuesta_id=id_materia_propuesta,
                    aula_id=h["aula_id"],
                    edificio_id=h["edificio_id"],
                    dia_semana=DiaSemanaEnum[h["dia"]],
                    hora_inicio=datetime.strptime(h["inicio"], "%H:%M").time(),
                    hora_fin=datetime.strptime(h["fin"], "%H:%M").time()
                )
                db.session.add(nuevo_horario)

        db.session.commit()
        return {"message": "Materia propuesta actualizada exitosamente"}

    def delete_materia_propuesta(self, id_materia_propuesta, data):
        materia = Materias_Propuestas.query.get(id_materia_propuesta)
        print(id_materia_propuesta)
        if not materia:
            return {"error": "Materia propuesta no encontrada", "status": 404}
        modificador_id = data.get("user_id")
        role = data.get("role")
        if modificador_id and not Usuarios.query.get(modificador_id):
            return {"error": "Usuario modificador no encontrado", "status": 404}
        if role not in ["COORDINADOR", "ADMIN"]:
            return {"error": "No autorizado. Solo coordinadores o administradores pueden eliminar", "status": 403}
        creador_id = materia.user_id
        creador = Usuarios.query.get(creador_id)
        notificacion_data = {
            "tipo": NotificacionesEnum.GRUPO_CANCELADO.name,
            "creador_grupo_id": modificador_id,
            "usuario_id": creador_id,
            "tipo_usuario": creador.rol.name,
            "materia_propuesta_id": id_materia_propuesta
        }
        notificacion_result = notificacionesService.create_notificacion(notificacion_data)
        if notificacion_result["status"] != 201:
            db.session.rollback()
        db.session.delete(materia)
        db.session.commit()
        return {"message": "Materia propuesta eliminada correctamente"}

    def get_by_status_and_carrera(self, status, clave_carrera):
        materias = (
            db.session.query(Materias_Propuestas)
            .filter(
                Materias_Propuestas.status == StatusEnum[status.upper()],
                Materias_Propuestas.clave_carrera == clave_carrera
            )
            .all()
        )

        return [self.serialize_materia(m) for m in materias]

    def get_by_status(self, status):
        materias = (
            db.session.query(Materias_Propuestas)
            .filter(Materias_Propuestas.status == StatusEnum[status.upper()])
            .all()
        )

        return [self.serialize_materia(m) for m in materias]

    def serialize_materia(self, materia):
        horarios = (
            db.session.query(Horario)
            .filter(Horario.materia_propuesta_id == materia.id_materia_propuesta)
            .all()
        )

        horarios_serializados = [
            {
                "id": h.id_horario,
                "dia": h.dia_semana.name,
                "inicio": h.hora_inicio.strftime("%H:%M"),
                "fin": h.hora_fin.strftime("%H:%M"),
                "aula_id": h.aula_id,
                "edificio_id": h.aula.edificio_id if h.aula else None
            }
            for h in horarios
        ]

        return {
            "id": materia.id_materia_propuesta,
            "materia_id": materia.materia_id,
            "clave_carrera": materia.clave_carrera,
            "status": materia.status.name,
            "turno": materia.turno.name if materia.turno else None,
            "docente": materia.docente,
            "cupo": materia.cupo,
            "creado_por": materia.user_id,
            "fecha_creacion": materia.fecha_creacion.isoformat(),
            "horarios": horarios_serializados
        }

    def get_by_carrera(self, clave_carrera):
        materias = (
            db.session.query(Materias_Propuestas)
            .filter(Materias_Propuestas.clave_carrera == clave_carrera)
            .all()
        )
        return [self.serialize_materia(m) for m in materias]

