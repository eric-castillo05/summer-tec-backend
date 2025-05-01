from flaskr.utils.db import db


class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.String(50), db.ForeignKey('usuarios.email'), nullable=False)
    materia_propuesta_id = db.Column(db.Integer, db.ForeignKey('materias_propuestas.id_materia_propuesta'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, nullable=False)
    estudiante = db.relationship('Estudiante', backref='registros')