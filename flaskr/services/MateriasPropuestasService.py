from datetime import datetime
from sqlalchemy.orm import aliased
from flaskr.models import Docente, StatusEnum, TurnoEnum, RolesEnum
from flaskr.services import EstudianteService
from flaskr.utils.db import db
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models.materias import Materias
from flaskr.models.aulas import Aula
from flaskr.models.coordinadores import Coordinadores
from flaskr.models.estudiante import Estudiante
from flaskr.models.admin import Admin

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
                Aula.aula_id.label("aula"),
                estudiante_alias.numero_control.label("creador_estudiante"),
                coordinador_alias.numero_control.label("creador_coordinador"),
                admin_alias.id.label("creador-admin")
            )
            .join(Materias_Propuestas, Materias.clave_materia == Materias_Propuestas.materia_id)
            .join(Docente, Materias_Propuestas.docente == Docente.id_docente, isouter=True)
            .join(Aula, Materias_Propuestas.aula_id == Aula.aula_id, isouter=True)
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
                "horario": materia.id_materia_propuesta,
                "profesor": materia.profesor,
                "nombre_materia": materia.nombre_materia,
                "aula": materia.aula,
                "creado_por": materia.creador_estudiante if materia.creador_estudiante else materia.creador_coordinador
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
            return {"error": "Provide exactly one creator: 'id_estudiante', 'id_coordinador', or 'id_admin'", "status": 400}

        # Check student creation limit
        if id_estudiante:
            result = self.estudiante_service.can_create_materia_propuesta(id_estudiante)
            if not result.get("can_create", False):
                return {"error": result.get("message", "Limit reached"), "status": 400}

        try:
            new_materia = Materias_Propuestas(
                materia_id=data["materia_id"],
                clave_carrera=data["clave_carrera"],
                status=StatusEnum[data["status"]],
                aula_id=data.get("aula_id"),
                turno=TurnoEnum[data["turno"]],
                fecha_creacion=datetime.now(),
                cupo=data.get("cupo", 25),
                docente=data.get("docente")
            )

            if id_estudiante:
                new_materia.id_estudiante = id_estudiante
            elif id_coordinador:
                new_materia.id_coordinador = id_coordinador
            elif id_admin:
                new_materia.id_admin = id_admin

            db.session.add(new_materia)
            db.session.commit()

            return {"message": "Materia propuesta registrada con éxito", "status": 201}

        except KeyError as e:
            return {"error": f"Invalid key: {str(e)}", "status": 400}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Something went wrong: {str(e)}", "status": 500}