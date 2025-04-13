from sqlalchemy import Enum, ForeignKeyConstraint
from flaskr.models import DiaSemanaEnum
from flaskr.utils.db import db


class Horario(db.Model):
    __tablename__ = 'horarios'

    id_horario = db.Column(db.Integer, primary_key=True)
    materia_propuesta_id = db.Column(db.Integer, db.ForeignKey('materias_propuestas.id_materia_propuesta'),
                                     nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.aula_id'), nullable=False)
    dia_semana = db.Column(Enum(DiaSemanaEnum), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    edificio_id = db.Column(db.String(3), nullable=False)
    # Relación con Aula (un Horario pertenece a un Aula)
    aula = db.relationship('Aula', backref='horarios_rel', lazy='joined')

    __table_args__ = (
        ForeignKeyConstraint(
            ['aula_id', 'edificio_id'],
            ['aulas.aula_id', 'aulas.edificio_id'],
        ),
    )

    # Relationship with Aula using the composite key
    aula = db.relationship('Aula',
                           foreign_keys=[aula_id, edificio_id],
                           primaryjoin="and_(Horario.aula_id==Aula.aula_id, "
                                       "Horario.edificio_id==Aula.edificio_id)",
                           backref='horarios')


