from flaskr.utils.db import db

class Coordinadores(db.Model):
    __tablename__ = 'coordinadores'
    numero_control = db.Column(db.String(10), primary_key=True, nullable=False)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carreras.clave_carrera'), nullable=False)
    nombre_carrera = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(50), nullable=False)