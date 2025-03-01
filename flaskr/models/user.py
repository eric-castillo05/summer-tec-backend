from flaskr.utils.db import db

class User(db.Model):
    __tablename__ = "users"
    numero_control = db.Column(db.String(9), primary_key=True)
    nombre_completo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<User {self.numero_control}>"