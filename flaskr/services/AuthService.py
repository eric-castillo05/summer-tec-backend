from datetime import timedelta

from flask import url_for, current_app, jsonify
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.utils import Config
from flaskr.utils.mail import mail
from flaskr.utils.db import db
from flaskr.models.estudiante import Estudiante
from flaskr.models.coordinadores import Coordinadores
from flaskr.models import RolesEnum, Admin
from flaskr.models import Usuarios
from flask_mail import Message

class AuthService:
    def __init__(self):
        pass

    def signup(self, numero_control, nombre_completo, email, password, phone_number, clave_carrera):
        if Estudiante.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

        if Estudiante.query.filter_by(numero_control=numero_control).first():
            return {"error": "Control number already registered"}, 400

        hashed_password = generate_password_hash(password)
        new_user = Estudiante(
            numero_control=numero_control,
            nombre_completo=nombre_completo,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            clave_carrera=clave_carrera,
            rol=RolesEnum.ESTUDIANTE
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # Create token with string identity and role as additional claim
            access_token = create_access_token(
                identity=str(new_user.email),
                additional_claims={"role": new_user.rol.value},
                expires_delta=timedelta(minutes=15)
            )
            return {"access_token": access_token}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def login(self, email, password):
        user = Estudiante.query.filter_by(email=email).first()
        clave_carrera = None

        if user:
            clave_carrera = user.clave_carrera

        else:
            user = Coordinadores.query.filter_by(email=email).first()

            if user:
                clave_carrera = user.clave_carrera
            else:
                user = Admin.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return {"error": "Invalid email or password"}, 401


        role = user.rol.value if hasattr(user, 'rol') and user.rol else "unknown"

        identity = str(user.email)

        access_token = create_access_token(
            identity=identity,
            additional_claims={
                "role": role,
            },
            expires_delta=timedelta(minutes=15)
        )

        return {
            "access_token": access_token,
            "user": {
                "nombre_completo": user.nombre_completo,
                "email": user.email,
                "role": role,
                "carrera": clave_carrera,
            }
        }, 200


    def change_password(self, email):
        user = Estudiante.query.filter_by(email=email).first()
        if not user:
            return {"error": "Email not registered"}, 400
        try:
            s = URLSafeTimedSerializer(Config.SECRET_KEY)
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth_bp.reset_password', token=token, _external=True)


            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Please click this link to reset your password: {reset_url}\nThis link will expire in 1 hour."
            )

            current_app.logger.info(f"Attempting to send email to: {email}")
            mail.send(msg)
            current_app.logger.info("Email sent successfully according to Flask-Mail")
            return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
        except Exception as e:
            current_app.logger.error(f"Email sending error: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return jsonify({"error": "Failed to send reset email"}), 500

    def reset_password(self, token, new_password):
        if not new_password or len(new_password) < 8:
            return jsonify({"message": "Password must be at least 8 characters", "success": False}), 400

        try:
            s = URLSafeTimedSerializer(Config.SECRET_KEY)
            email = s.loads(token, salt='password-reset-salt', max_age=3600)
        except Exception:
            return jsonify({"message": "Invalid or expired reset link", "success": False}), 400

        user = Usuarios.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "User not found", "success": False}), 404

        try:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"message": "Password reset successful! Redirecting to login...", "success": True}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to reset password. Please try again.", "success": False}), 500
