from flaskr.models.estudiante import Estudiante
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models import RolesEnum


class EstudianteService:
    def __init__(self):
        pass

    def can_create_materia_propuesta(self, estudiante_id):
        """
        Returns True if the student can create another MateriaPropuesta.
        Students are limited to 2 proposals.
        """
        estudiante = Estudiante.query.filter_by(numero_control=estudiante_id).first()

        if not estudiante:
            return {"can_create": False, "message": "Student not found"}

        if estudiante.rol != RolesEnum.ESTUDIANTE:
            return {"can_create": True, "message": "Only students are limited"}

        count = Materias_Propuestas.query.filter_by(id_estudiante=estudiante.numero_control).count()

        if count >= 2:
            return {"can_create": False, "message": "Maximum number of proposed subjects reached (2)."}

        return {"can_create": True}