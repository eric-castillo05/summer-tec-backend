from flaskr.models.usuarios import Usuarios
from flaskr.utils.db import db

class Coordinadores(Usuarios):
    __tablename__ = "coordinadores"

    email = db.Column(db.String(50), db.ForeignKey('usuarios.email'), primary_key=True)
    numero_control = db.Column(db.String(10), unique=True, nullable=False)
    clave_carrera = db.Column(db.String(50), db.ForeignKey('carreras.clave_carrera'), nullable=False)

    def __repr__(self):
        return f"<Coordinador {self.email}>"
