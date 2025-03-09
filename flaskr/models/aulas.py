from flaskr.utils.db import db

class Aula(db.Model):
    __tablename__ = 'aulas'
    aula_id = db.Column(db.Integer, primary_key=True)
    edificio_id = db.column(db.String(10), db.ForeignKey('edificios.numero_edificio'))