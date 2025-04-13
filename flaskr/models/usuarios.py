import uuid
from sqlalchemy import Enum
from flaskr.utils.db import db
from flaskr.models.enums import RolesEnum

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_completo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    rol = db.Column(Enum(RolesEnum), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.email}>"
