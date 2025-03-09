from enum import Enum
from flaskr.utils.db import db
from flaskr.models.enums import TurnoEnum, StatusEnum

class Materias_Propuestas(db.Model):
    __tablename__ = 'materias_propuestas'
    id_materia_propuesta = db.Column(db.Integer, primary_key=True)
    id_estuditante = db.Column(db.String(9), db.ForeignKey('user.numero_control') ,nullable=True)
    id_coordinador = db.Column(db.String(10), db.ForeignKey('coordinadores.numero_control'), nullable=True)
    materia_id = db.Column(db.String(15), db.ForeignKey('materias.clave_materia'), nullable=False)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carrera.carrera'), nullable=False)
    status = db.Column(Enum(StatusEnum), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('aula.aula_id'), nullable=False)
    turno = db.Column(Enum(TurnoEnum), nullable=False)
    cupo = db.Column(db.Integer, nullable=False)
    fecha_creaciobn = db.Column(db.DateTime, nullable=False)

