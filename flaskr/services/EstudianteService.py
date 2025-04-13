from datetime import datetime
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models.estudiante import Estudiante
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models import RolesEnum, Registro, StatusEnum, Usuarios
from flaskr.utils.db import db


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

    def inscribir_estudiante(self, estudiante_id, materia_propuesta_id):
        existe = Registro.query.filter_by(
            estudiante_id=estudiante_id,
            materia_propuesta_id=materia_propuesta_id
        ).first()

        if existe:
            return {"error": "Ya estás inscrito en esta materia", "status": 400}

        # Obtener la materia propuesta
        materia = Materias_Propuestas.query.get(materia_propuesta_id)

        if not materia:
            return {"error": "La materia propuesta no existe", "status": 404}

        if materia.status == StatusEnum.RECHAZADO:
            return {"error": "No puedes inscribirte en una materia rechazada", "status": 400}

        # Verificar cupo
        if materia.cupo <= 0:
            return {"error": "No hay cupo disponible en esta materia", "status": 400}

        if existe:
            return {"error": "Ya estás inscrito en esta materia", "status": 400}

        inscripcion = Registro(
            estudiante_id=estudiante_id,
            materia_propuesta_id=materia_propuesta_id,
            fecha_inscripcion=datetime.now(),
        )
        db.session.add(inscripcion)
        materia.cupo -= 1
        db.session.commit()
        return {"message": "Inscripción exitosa", "status": 201}

    def baja_estudiante(self, estudiante_id, materia_propuesta_id):
        registro = Registro.query.filter_by(
            estudiante_id=estudiante_id,
            materia_propuesta_id=materia_propuesta_id
        ).first()

        if not registro:
            return {"error": "No estás inscrito en esta materia", "status": 404}

        materia = Materias_Propuestas.query.get(materia_propuesta_id)
        if not materia:
            return {"error": "La materia propuesta no existe", "status": 404}

        db.session.delete(registro)
        materia.cupo += 1
        db.session.commit()

        return {"message": "Baja exitosa", "status": 200}

    def obtener_estudiantes_inscritos(self, materia_propuesta_id):
        registros = Registro.query.filter_by(materia_propuesta_id=materia_propuesta_id).all()

        estudiantes_data = []
        for reg in registros:
            estudiante = Estudiante.query.filter_by(numero_control=reg.estudiante_id).first()
            if estudiante:
                estudiantes_data.append({
                    "numero_control": estudiante.numero_control,
                    "nombre_completo": estudiante.nombre_completo,
                    "email": estudiante.email,
                    "fecha_inscripcion": reg.fecha_inscripcion.strftime('%Y-%m-%d %H:%M:%S')
                })

        return estudiantes_data


