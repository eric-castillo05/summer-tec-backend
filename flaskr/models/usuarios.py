from flaskr.utils.db import db
from flaskr.models.enums import RolesEnum
from sqlalchemy import Enum

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    email = db.Column(db.String(50), primary_key=True)
    nombre_completo = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    rol = db.Column(Enum(RolesEnum), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.email}>"
