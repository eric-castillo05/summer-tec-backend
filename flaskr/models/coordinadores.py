from flaskr.models.usuarios import Usuarios
from flaskr.utils.db import db

class Coordinadores(Usuarios):
    id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), primary_key=True)
    numero_control = db.Column(db.String(10), unique=True, nullable=False)
    clave_carrera = db.Column(db.String(50), db.ForeignKey('carreras.clave_carrera'), nullable=False)

    def __repr__(self):
        return f"<Coordinador {self.numero_control}>"