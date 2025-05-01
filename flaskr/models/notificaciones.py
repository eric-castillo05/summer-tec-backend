from flaskr.utils.db import db
from sqlalchemy import Enum
from flaskr.models import NotificacionesEnum, RolesEnum

class Notificaciones(db.Model):
    __tablename__ = 'notificaciones'
    id_notificacion = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(Enum(NotificacionesEnum), nullable=False)
    creador_grupo_id = db.Column(db.String(50), db.ForeignKey('usuarios.email'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.String(50), db.ForeignKey('usuarios.email'), nullable=False)
    tipo_usuario = db.Column(Enum(RolesEnum), nullable=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)
    materia_propuesta_id = db.Column(db.Integer, db.ForeignKey('materias_propuestas.id_materia_propuesta'),
                                     nullable=True)

    creador = db.relationship('Usuarios', foreign_keys=[creador_grupo_id], backref='notificaciones_creadas')
    usuario = db.relationship('Usuarios', foreign_keys=[usuario_id], backref='notificaciones_recibidas')
    materia_propuesta = db.relationship('Materias_Propuestas', foreign_keys=[materia_propuesta_id],
                                        backref='notificaciones')

    def __repr__(self):
        return f"<Notificacion {self.id_notificacion} - {self.tipo} para {self.usuario_id}>"