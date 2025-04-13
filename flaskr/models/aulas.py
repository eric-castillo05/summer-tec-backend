from flaskr.utils.db import db

class Aula(db.Model):
    __tablename__ = 'aulas'
    aula_id = db.Column(db.Integer)
    edificio_id = db.Column(db.String(3), db.ForeignKey('edificios.numero_edificio'))

    __table_args__ = (
        db.PrimaryKeyConstraint('aula_id', 'edificio_id'),
    )