from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flaskr.routes.AuthRoutes import auth_bp
from flaskr.routes.DocentesRoutes import docentes_bp
from flaskr.routes.EstudinteRoutes import estudiante_bp
from flaskr.routes.MateriasPropuestasRoutes import materias_propuestas_bp
from flaskr.routes.MateriasRoute import materias_bp
from flaskr.routes.NotificacionesRoute import notificaciones_bp
from flaskr.utils.JWT import JWT
from flaskr.utils.config import Config
from flaskr.utils.db import Database, db
from flaskr.utils.mail import mail

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": Config.ROUTE}}, supports_credentials=True)
    Database().init_app(app)
    migrate.init_app(app, db)
    jwt = JWT(app)
    app.config['MAIL_SERVER'] = Config.MAIL_SERVER
    app.config['MAIL_PORT'] = Config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    mail.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(materias_propuestas_bp, url_prefix='/materias_propuestas')
    app.register_blueprint(materias_bp, url_prefix='/materias')
    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')
    app.register_blueprint(docentes_bp, url_prefix='/docente')
    app.register_blueprint(notificaciones_bp, url_prefix='/notificaciones')

    return app