from flaskr.utils.db import db
from flaskr.models.enums import TurnoEnum, StatusEnum
from sqlalchemy import Enum


class Materias_Propuestas(db.Model):
    __tablename__ = 'materias_propuestas'
    id_materia_propuesta = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.String(9), db.ForeignKey('estudiante.numero_control') ,nullable=True)
    id_coordinador = db.Column(db.String(35), db.ForeignKey('coordinadores.numero_control'), nullable=True)
    id_admin = db.Column(db.String(10), db.ForeignKey('admins.id'), nullable=True)
    materia_id = db.Column(db.String(15), db.ForeignKey('materias.clave_materia'), nullable=False)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carreras.clave_carrera'), nullable=False)
    status = db.Column(Enum(StatusEnum), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.aula_id'), nullable=True)
    turno = db.Column(Enum(TurnoEnum), nullable=True)
    cupo = db.Column(db.Integer, nullable=False)
    docente = db.Column(db.String(15), db.ForeignKey('docentes.id_docente'),nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)

