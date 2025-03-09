from flaskr.utils.db import db

class Carreras(db.Model):
    __tablename__ = 'carreras'
    clave_carrera = db.Column(db.String(15), primary_key=True)
    coordinador_id = db.column(db.String(10), db.ForeignKey('coordinadores.numero_control'))
    fecha = db.Column(db.DateTime, nullable=False)