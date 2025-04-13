from flaskr.utils.db import db


class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.String(9), db.ForeignKey('estudiante.numero_control'), nullable=False)
    materia_propuesta_id = db.Column(db.Integer, db.ForeignKey('materias_propuestas.id_materia_propuesta'), nullable=False)
    estudiante = db.relationship('Estudiante', backref='registros')
    materia_propuesta = db.relationship('Materias_Propuestas', backref='registros')
