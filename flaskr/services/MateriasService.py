from flaskr.utils.db import db
from flaskr.models.materias import Materias

class MateriasService:
    def __init__(self):
        pass

    def get_materias(self):
        materias = (
            db.session.query(
                Materias.nombre_materia,
                Materias.creditos,
                Materias.horas_semana
            ).all()
        )

        return [
            {
                "nombre_materia": materia.nombre_materia,
                "creditos": materia.creditos,
                "horas_semana": materia.horas_semana
            } for materia in materias
        ]