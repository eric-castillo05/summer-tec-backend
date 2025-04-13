from datetime import datetime, time
from sqlalchemy.orm import aliased
from flaskr.models import Docente, StatusEnum, TurnoEnum, RolesEnum, Registro, Horario, horario
from flaskr.services import EstudianteService
from flaskr.utils.db import db
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models.materias import Materias
from flaskr.models.aulas import Aula
from flaskr.models.coordinadores import Coordinadores
from flaskr.models.estudiante import Estudiante
from flaskr.models.admin import Admin
from flaskr.models.horario import DiaSemanaEnum


class MateriasPropuestasService:
    def __init__(self):
        self.estudiante_service = EstudianteService()

    def get_materias_propuestas(self):
        estudiante_alias = aliased(Estudiante)
        coordinador_alias = aliased(Coordinadores)
        admin_alias = aliased(Admin)

        materias = (
            db.session.query(
                Materias.horas_semana,
                Materias.creditos,
                Materias_Propuestas.cupo,
                Materias_Propuestas.turno,
                Materias_Propuestas.id_materia_propuesta,
                Docente.nombre_completo.label("profesor"),
                Materias.nombre_materia,
                estudiante_alias.numero_control.label("creador_estudiante"),
                coordinador_alias.numero_control.label("creador_coordinador"),
                admin_alias.id.label("creador-admin")
            )
            .join(Materias_Propuestas, Materias.clave_materia == Materias_Propuestas.materia_id)
            .join(Docente, Materias_Propuestas.docente == Docente.id_docente, isouter=True)
            .outerjoin(estudiante_alias, Materias_Propuestas.id_estudiante == estudiante_alias.numero_control)
            .outerjoin(coordinador_alias, Materias_Propuestas.id_coordinador == coordinador_alias.numero_control)
            .outerjoin(admin_alias, Materias_Propuestas.id_admin == admin_alias.id)
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
                "creado_por": materia.creador_estudiante if materia.creador_estudiante else (
                    materia.creador_coordinador if materia.creador_coordinador else "ADMIN")
            }
            for materia in materias
        ]

    def register_materia_propuesta(self, data):
        id_estudiante = data.get("id_estudiante")
        id_coordinador = data.get("id_coordinador")
        id_admin = data.get("id_admin")

        # Check that only one creator type is provided
        creators = [c for c in [id_estudiante, id_coordinador, id_admin] if c]
        if len(creators) != 1:
            return {"error": "Provide exactly one creator: 'id_estudiante', 'id_coordinador', or 'id_admin'",
                    "status": 400}

        # Check student creation limit
        if id_estudiante:
            result = self.estudiante_service.can_create_materia_propuesta(id_estudiante)
            if not result.get("can_create", False):
                return {"error": result.get("message", "Limit reached"), "status": 400}

        try:
            new_materia = Materias_Propuestas(
                materia_id=data["materia_id"],
                clave_carrera=data["clave_carrera"],
                status=StatusEnum['PENDIENTE'],
                turno=TurnoEnum[data["turno"]],
                fecha_creacion=datetime.now(),
                cupo=data.get("cupo", 25),
                docente=data.get("docente"),
            )

            # Assign the creator based on the provided ID
            if id_estudiante:
                new_materia.id_estudiante = id_estudiante
            elif id_coordinador:
                new_materia.id_coordinador = id_coordinador
            elif id_admin:
                new_materia.id_admin = id_admin  # Admin does not need control number

            db.session.add(new_materia)
            db.session.flush()
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
                "horarios": [
                    {
                        "id_horario": h.id_horario,
                        "dia": h.dia_semana.name,
                        "inicio": h.hora_inicio.strftime("%H:%M"),
                        "fin": h.hora_fin.strftime("%H:%M"),
                        "aula_id": h.aula_id
                    }
                    for h in saved_horarios
                ]
            }

        except KeyError as e:
            return {"error": f"Invalid key: {str(e)}", "status": 400}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Something went wrong: {str(e)}", "status": 500}

    def update_materia_propuesta(self, id_materia_propuesta, data):
        materia = Materias_Propuestas.query.get(id_materia_propuesta)

        if not materia:
            return {"error": "Materia propuesta no encontrada", "status": 404}

        # Actualización de campos simples
        if "aula_id" in data:
            materia.aula_id = data["aula_id"]
        if "status" in data:
            materia.status = StatusEnum(data["status"])
        if "docente" in data:
            materia.docente = data["docente"]

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

    def delete_materia_propuesta(self, id_materia_propuesta):
        materia = Materias_Propuestas.query.get(id_materia_propuesta)

        if not materia:
            return {"error": "Materia propuesta no encontrada", "status": 404}

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
            "creado_por": materia.id_estudiante or materia.id_coordinador or materia.id_admin,
            "fecha_creacion": materia.fecha_creacion.isoformat(),
            "horarios": horarios_serializados
        }

    def inscribir_estudiante(self, estudiante_id, materia_propuesta_id):
        # Verificar duplicados
        existe = Registro.query.filter_by(
            estudiante_id=estudiante_id,
            materia_propuesta_id=materia_propuesta_id
        ).first()

        if existe:
            return {"error": "Ya estás inscrito en esta materia", "status": 400}

        inscripcion = Registro(
            estudiante_id=estudiante_id,
            materia_propuesta_id=materia_propuesta_id
        )
        db.session.add(inscripcion)
        db.session.commit()
        return {"message": "Inscripción exitosa", "status": 201}

