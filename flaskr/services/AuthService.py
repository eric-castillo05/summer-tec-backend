from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.utils.db import db
from flaskr.models.user import User
from flaskr.models.coordinadores import Coordinadores


class AuthService:
    def __init__(self):
        pass

    def signup(self, numero_control, nombre_completo, email, password, phone_number):
        if User.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

        if User.query.filter_by(numero_control=numero_control).first():
            return {"error": "Control number already registered"}, 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            numero_control=numero_control,
            nombre_completo=nombre_completo,
            email=email,
            password=hashed_password,
            phone_number=phone_number
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=numero_control)
            return {"access_token": access_token}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def login(self, email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid email or password"}, 401

        user = User.query.filter_by(email=email).first()
        if not user:
            user = Coordinadores.query.filter_by(email=email).first()

        access_token = create_access_token(identity=user.numero_control)
        return {"access_token": access_token}, 200