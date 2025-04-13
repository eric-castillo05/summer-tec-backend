from flaskr.models.usuarios import Usuarios
from flaskr.utils.db import db

class Estudiante(Usuarios):
    __tablename__ = "estudiante"
    id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), primary_key=True)
    numero_control = db.Column(db.String(9), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Estudiante {self.numero_control}>"