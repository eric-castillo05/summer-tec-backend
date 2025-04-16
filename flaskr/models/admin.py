from flaskr.models.usuarios import Usuarios
from flaskr.utils.db import db

class Admin(Usuarios):
    __tablename__ = 'admins'

    email = db.Column(db.String(50), db.ForeignKey('usuarios.email'), primary_key=True)

    def __repr__(self):
        return f"<Admin {self.email}>"
