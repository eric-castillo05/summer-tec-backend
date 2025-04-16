import uuid

from flaskr.models import Docente
from flaskr.utils.db import db


class DocenteService:
    def __init__(self):
        pass

    def get_all(self, clave_carrera):
        docentes = Docente.query.filter_by(clave_carrera=clave_carrera).all()

        return [
            {
                "nombre_completo": docente.nombre_completo,
                "email": docente.email,
                "clave_carrera": docente.clave_carrera
            } for docente in docentes
        ]

    def create_docente(self, data):
        required_fields = ['nombre_completo', 'clave_carrera', 'email']
        if not all(field in data for field in required_fields):
            return {"error": "Faltan campos obligatorios", "status": 400}

        # Verificar si ya existe el email
        existing_docente = Docente.query.filter_by(email=data['email']).first()
        if existing_docente:
            return {"error": "El email ya está registrado", "status": 409}

        new_docente = Docente(
            nombre_completo=data['nombre_completo'],
            clave_carrera=data['clave_carrera'],
            email=data['email']
        )

        db.session.add(new_docente)
        db.session.commit()

        return {
            "message": "Docente creado exitosamente",
            "docente": {
                "nombre_completo": new_docente.nombre_completo,
                "clave_carrera": new_docente.clave_carrera,
                "email": new_docente.email
            },
            "status": 201
        }