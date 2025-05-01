from datetime import datetime
from flaskr.models.estudiante import Estudiante
from flaskr.models.materias_propuestas import Materias_Propuestas
from flaskr.models import RolesEnum, Registro, StatusEnum, Materias, Docente, Usuarios, Edificios, Horario, Aula, \
    Notificaciones, estudiante, NotificacionesEnum
from flaskr.routes.NotificacionesRoute import notificacionesService
from flaskr.utils.db import db



class EstudianteService:
    def __init__(self):
        pass

    def can_create_materia_propuesta(self, estudiante_id):
        """
        Returns True if the student can create another MateriaPropuesta.
        Students are limited to 2 proposals.
        """
        estudiante = Estudiante.query.filter_by(email=estudiante_id).first()

        if not estudiante:
            return {"can_create": False, "message": "Student not found"}

        if estudiante.rol != RolesEnum.ESTUDIANTE:
            return {"can_create": True, "message": "Only students are limited"}

        count = Materias_Propuestas.query.filter_by(user_id=estudiante.email).count()

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

        if materia.cupo == 30:
            data = {
                "tipo": NotificacionesEnum.GRUPO_ACTUALIZADO.name,
                "creador_grupo_id": estudiante_id,
                "usuario_id": estudiante_id,
                "tipo_usuario": RolesEnum.ESTUDIANTE.name,
                "materia_propuesta_id": materia_propuesta_id,
            }
            notificacion_result = notificacionesService.create_notificacion(data)
            if notificacion_result["status"] != 201:
                db.session.rollback()

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
            estudiante = Estudiante.query.filter_by(email=reg.estudiante_id).first()
            if estudiante:
                estudiantes_data.append({
                    "nombre_completo": estudiante.nombre_completo,
                    "email": estudiante.email,
                    "fecha_inscripcion": reg.fecha_inscripcion.strftime('%Y-%m-%d %H:%M:%S')
                })

        return estudiantes_data

    def obtener_mis_grupos(self, estudiante_id) :
        materias = (
            db.session.query(
                Materias.horas_semana,
                Materias.creditos,
                Materias_Propuestas.turno,
                Materias_Propuestas.id_materia_propuesta,
                Docente.nombre_completo.label('profesor'),
                Materias.nombre_materia,
                Materias.clave_materia,
                Materias.clave_carrera,
                Usuarios.nombre_completo,
                Edificios.numero_edificio.label('edificio'),
                Materias_Propuestas.status
            )
            .join(Registro, Registro.materia_propuesta_id == Materias_Propuestas.id_materia_propuesta)
            .join(Materias, Materias_Propuestas.materia_id == Materias.clave_materia)
            .outerjoin(Docente, Materias_Propuestas.docente == Docente.email)
            .join(Usuarios, Materias_Propuestas.user_id == Usuarios.email)
            .outerjoin(Horario, Horario.materia_propuesta_id == Materias_Propuestas.id_materia_propuesta)
            .outerjoin(Aula, Horario.aula_id == Aula.aula_id)
            .outerjoin(Edificios, Aula.edificio_id == Edificios.numero_edificio)
            .filter(Registro.estudiante_id == estudiante_id)
            .all()
        )
        if not materias:
            return {"error": "No estas inscrito en esta materia", "status": 404}
        result = [
            {
                "horas_semana": m.horas_semana,
                "creditos": m.creditos,
                "turno": m.turno.value if m.turno else None,
                "id_materia_propuesta": m.id_materia_propuesta,
                "profesor": m.profesor,
                "nombre_materia": m.nombre_materia,
                "clave_materia": m.clave_materia,
                "clave_carrera": m.clave_carrera,
                "nombre_usuario": m.nombre_completo,
                "edificio": m.edificio,
                "status": m.status.value if m.status else None
            }
            for m in materias
        ]

        return {"grupos": result, "status": 200}

