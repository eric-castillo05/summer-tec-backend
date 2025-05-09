from datetime import timedelta

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.utils.db import db
from flaskr.models.estudiante import Estudiante
from flaskr.models.coordinadores import Coordinadores
from flaskr.models import RolesEnum, Admin


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