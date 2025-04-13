from flaskr.utils.db import db


class Docente(db.Model):
    __tablename__ = 'docentes'
    id_docente = db.Column(db.String(25), primary_key=True)
    nombre_completo = db.Column(db.String(50), nullable=False)
    clave_carrera = db.Column(db.String(15), db.ForeignKey('carreras.clave_carrera'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
