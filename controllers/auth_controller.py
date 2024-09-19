from datetime import timedelta

from flask import Blueprint, jsonify, request

from models.user import User, user_schema, users_schema, user_schema_validation
from init import bcrypt, db

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from utils.authorization import authorize_as_admin

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


#get all users
@auth_bp.route("/all")
@jwt_required()
def get_all_users():
    if authorize_as_admin():
        statement = db.select(User)
        users = db.session.scalars(statement)
        return jsonify(users_schema.dump(users))
    else:
        return {"error":"Not authorized to perform this action!"}


@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body = user_schema_validation.load(request.get_json())
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
        return {"error":"the email does NOT exit!"}, 400
    
    password = body.get("password")
    if password:
        if bcrypt.check_password_hash(user.password, password):
            token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
            return {"ACCESS GRANTED": {"email": user.email, "is_admin": user.is_admin, "token": token}}
        else:
            # Respond back with an error message
            return {"error": "Invalid password"}, 400
    else:
        return {"error":"Enter a valid password"}, 400
    
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    body = user_schema_validation.load(request.get_json(), partial=True)
    password = body.get("password")
    # fetch the user from the db
    statement = db.select(User).filter_by(user_id=get_jwt_identity())
    user = db.session.scalar(statement)
    # update the user fields if the user is found in the database
    if user:
        user.name = body.get("name") or user.name
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.commit()
        return jsonify({"message": "User info updated successfully!"}, user_schema.dump(user))
    else:
        return {"error":f"User {get_jwt_identity()} does NOT exist"}