from flaskr.utils.db import db


class Docente(db.Model):
    __tablename__ = 'docentes'
    id_docente = db.Column(db.String(25), primary_key=True)
    nombre_completo = db.Column(db.String(15), nullable=False)
    area = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)