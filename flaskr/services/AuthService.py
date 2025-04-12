from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.utils.db import db
from flaskr.models.estudiante import Estudiante
from flaskr.models.coordinadores import Coordinadores
from flaskr.models import RolesEnum


class AuthService:
    def __init__(self):
        pass

    def signup(self, numero_control, nombre_completo, email, password, phone_number):
        if Estudiante.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

        if Estudiante.query.filter_by(numero_control=numero_control).first():
            return {"error": "Control number already registered"}, 400

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = Estudiante(
            numero_control=numero_control,
            nombre_completo=nombre_completo,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            rol=RolesEnum.ESTUDIANTE
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # Create token with string identity and role as additional claim
            access_token = create_access_token(
                identity=str(new_user.numero_control),
                additional_claims={"role": new_user.rol.value}
            )
            return {"access_token": access_token}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def login(self, email, password):
        # First try to find user in Estudiante table
        user = Estudiante.query.filter_by(email=email).first()
        user_type = "estudiante"

        # If not found, try Coordinadores table
        if not user:
            user = Coordinadores.query.filter_by(email=email).first()
            user_type = "coordinador"

        # If still not found or password doesn't match, return error
        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid email or password"}, 401

        # Get the role value from enum
        role = user.rol.value if hasattr(user, 'rol') and user.rol else "unknown"

        # Use the numero_control as the identity (as string)
        identity = str(user.numero_control)

        # Create token with string identity
        access_token = create_access_token(
            identity=identity,
            additional_claims={
                "role": role,
                "user_type": user_type
            }
        )

        return {
            "access_token": access_token,
            "user": {
                "numero_control": user.numero_control,
                "nombre_completo": user.nombre_completo,
                "email": user.email,
                "role": role,
                "user_type": user_type
            }
        }, 200