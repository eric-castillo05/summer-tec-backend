from datetime import datetime

from sqlalchemy.orm import aliased

from flaskr.models import Docente, StatusEnum, TurnoEnum
from flaskr.utils.db import db
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models.materias import Materias
from flaskr.models.aulas import Aula
from flaskr.models.coordinadores import Coordinadores
from flaskr.models.estudiante import Estudiante

class MateriasPropuestasService:
    def __init__(self):
        pass

    def get_materias_propuestas(self):
        estudiante_alias = aliased(Estudiante)
        coordinador_alias = aliased(Coordinadores)

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
                coordinador_alias.numero_control.label("creador_coordinador")
            )
            .join(Materias_Propuestas, Materias.clave_materia == Materias_Propuestas.materia_id)
            .join(Docente, Materias_Propuestas.id_coordinador == Docente.id_docente, isouter=True)
            .join(Aula, Materias_Propuestas.aula_id == Aula.aula_id, isouter=True)
            .outerjoin(estudiante_alias, Materias_Propuestas.id_estudiante == estudiante_alias.numero_control)
            .outerjoin(coordinador_alias, Materias_Propuestas.id_coordinador == coordinador_alias.numero_control)
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

        if data.get('cupo') == 25:
            return {"error": "Group full"}

        if bool(id_estudiante) == bool(id_coordinador):
            return {"error": "Provide only one: either 'id_estudiante' or 'id_coordinador'", "status": 400}
        try:
            new_materia = Materias_Propuestas(
                materia_id=data["materia_id"],
                clave_carrera=data["clave_carrera"],
                status=StatusEnum[data["status"]],
                aula_id=data.get("aula_id"),
                turno=TurnoEnum[data["turno"]],
                fecha_creacion=datetime.now(),
                cupo=data["cupo"]
            )
            if id_estudiante:
                new_materia.id_estudiante = id_estudiante
            elif id_coordinador:
                new_materia.id_coordinador = id_coordinador

            db.session.add(new_materia)
            db.session.commit()

            return {"message": "Materia propuesta registrada con éxito", "status": 201}

        except KeyError as e:
            return {"error": f"Invalid key: {str(e)}", "status": 400}

        except Exception as e:
            db.session.rollback()
            return {"error": f"Something went wrong: {str(e)}", "status": 500}