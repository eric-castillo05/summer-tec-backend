from flaskr.models.usuarios import Usuarios
from flaskr.utils.db import db


class Admin(Usuarios):
    __tablename__ = 'admins'

    id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), primary_key=True)

    def __repr__(self):
        return f"<Admin {self.email}>"
