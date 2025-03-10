from flaskr.utils.db import db

class Carreras(db.Model):
    __tablename__ = 'carreras'
    clave_carrera = db.Column(db.String(15), primary_key=True)
    nombre_carrera = db.Column(db.String(15), nullable=False)
