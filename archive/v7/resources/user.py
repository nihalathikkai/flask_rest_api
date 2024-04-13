from datetime import timedelta
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(schema=UserSchema)
    def post(self, request_data):
        username = request_data.get("username")
        password = request_data.get("password")

        if not username or not password:
            abort(400, message="Username or password is empty.")

        if len(password) < 8:
            abort(400, message="Password too small.")

        if UserModel.query.filter(UserModel.username == username).first():
            abort(409, message="Username already exists.")

        user = UserModel(
            username=username,
            password=pbkdf2_sha256.hash(password),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Error occured while adding user.: {e}")

        return {"message": "User created."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(schema=UserSchema)
    def post(self, request_data):
        username = request_data.get("username")
        password = request_data.get("password")

        user = UserModel.query.filter(UserModel.username == username).first()

        if not user or not pbkdf2_sha256.verify(password, user.password):
            abort(401, message="Username or password is incorrect.")

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(1))

        return {"access_token": access_token, "refresh_token": refresh_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        return {"message": "User logged out."}


@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, schema=UserSchema)
    def get(self, user_id):
        if get_jwt_identity() != user_id:
            abort(403, message="You don't have permission to access this resource.")
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        if get_jwt_identity != user_id:
            abort(403, message="You don't have permission to access this resource")
        UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user_id)
            db.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Error occured while deleting user.: {e}")

        return {"message": "User deleted."}
