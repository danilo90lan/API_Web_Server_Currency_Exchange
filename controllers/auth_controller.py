from datetime import timedelta

from flask import Blueprint, jsonify, request

from models.user import User, user_schema
from init import bcrypt, db

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body = request.get_json()
        password = body.get("password")
        
        # Create an instance of the User Model
        user = User(
            name = body.get("name"),
            email = body.get("email"),
            password = bcrypt.generate_password_hash(password).decode("utf-8")
        )
        # Add and commit to the DB
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}, user_schema.dump(user)), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation
            return {"error": "Email address must be unique"}, 400
        
    except ValueError as err:
        # Handle the empty password error
        if str(err) == "Password must be non-empty.":
            return {"error": "Password must be non-empty"}, 400
        
@auth_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    statement = db.select(User).filter_by(email=body.get("email"))
    user = db.session.scalar(statement)

    if not user:
        return {"error":"the email does NOT exit!"}

    if bcrypt.check_password_hash(user.password, body.get("password")):
         # create JWT
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
        return {"ACCESS GRANTED": {"email": user.email, "is_admin": user.is_admin, "token": token}}