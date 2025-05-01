from flaskr.utils.db import db
from flaskr.models.enums import TurnoEnum, StatusEnum
from sqlalchemy import Enum


class Materias_Propuestas(db.Model):
    __tablename__ = 'materias_propuestas'
    id_materia_propuesta = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('usuarios.email'), nullable=False)
    materia_id = db.Column(db.String(15), db.ForeignKey('materias.clave_materia'), nullable=False)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carreras.clave_carrera'), nullable=False)
    status = db.Column(Enum(StatusEnum), nullable=False)
    turno = db.Column(Enum(TurnoEnum), nullable=True)
    cupo = db.Column(db.Integer, nullable=False)
    docente = db.Column(db.String(50), db.ForeignKey('docentes.email'),nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)

    horarios = db.relationship('Horario', backref='materia_propuesta', lazy='joined',
                               cascade="all, delete-orphan")
    registros = db.relationship('Registro', backref='materia_propuesta', lazy='joined',
                               cascade="all, delete-orphan")
    materia = db.relationship('Materias', foreign_keys=[materia_id], lazy='joined')
    docente_rel = db.relationship('Docente', foreign_keys=[docente], lazy='joined')
    usuario = db.relationship('Usuarios', backref='materias_propuestas')

