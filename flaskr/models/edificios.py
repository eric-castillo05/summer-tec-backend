from flaskr.utils.db import db

class Edificios(db.Model):
    __tablename__ = 'edificios'

    numero_edificio = db.Column(db.String(3), primary_key=True)
    numero_aulas = db.Column(db.Integer)

    aulas = db.relationship('Aula', back_populates='edificio', lazy='joined',
                          foreign_keys="Aula.edificio_id")