from flaskr.utils.db import db

class Materias(db.Model):
    __tablename__ = 'materias'
    clave_materia = db.Column(db.String(15), primary_key=True)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carreras.clave_carrera'))
    nombre_materia = db.Column(db.String(50), nullable=False)
    creditos = db.Column(db.Integer, nullable=False)
    horas_semana = db.Column(db.Integer, nullable=False)