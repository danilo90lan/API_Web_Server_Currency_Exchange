# Import timedelta for token expiration time
from datetime import timedelta

# Import Flask modules for creating blueprints and handling requests/responses
from flask import Blueprint, jsonify, request

from models.user import User, user_schema, users_schema, user_schema_validation
from models.account import Account, accounts_schema
# Import bcrypt for password hashing and db for database operations
from init import bcrypt, db

# Import SQLAlchemy error handling and PostgreSQL error codes
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes
# Import Forbidden exception for unauthorized access
from werkzeug.exceptions import Forbidden
# JWT handling for authentication
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Import custom authorization utility
from utils.authorization import authorize_as_admin

# Create a Blueprint for auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# get all users
@auth_bp.route("/all")
@jwt_required()     # Ensure that only authenticated users can access this route
def get_all_users():
    """
    Fetches and returns all user records from the database, 
    ensuring that only users with admin privileges can access this information.

    Returns:
        JSON response containing the list of users.
    Raises:
        Forbidden: If the user does not have admin privileges.
    """
    # Check if the user has admin privileges
    if authorize_as_admin():
        # Create a SQL statement to select all users

        # SELECT *
        # FROM User;
        statement = db.select(User)
        users = db.session.scalars(statement)
        # Return a JSON response
        return jsonify(users_schema.dump(users))
    else:
        # Raise a Forbidden error if the user is not authorized
        raise Forbidden("You do not have permission to access this resource.")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    User registration by validating input, 
    securely hashing passwords, creating a new user record.

    Returns:
        JSON response indicating success or failure of the registration.
    Raises:
        400: If there are validation errors.
        409: If the email is already registered.
    """
    try:
        # Load and validate the incoming JSON data against the schema
        # 'request.get_json()' retrieves the incoming JSON payload from the client
        body = user_schema_validation.load(request.get_json())
        # Extract the password from the validated JSON data
        password = body.get("password")

        # Create an instance of the User Model
        user = User(
            # Capitalize the user's name for consistency
            name=body.get("name").strip().capitalize(),
            # Convert email address to lowercase to ensure case-insensitivity when comparing email addresses.
            email=body.get("email").strip().lower(),                  
            # Hash the password securely with bcrypt and decode it to a UTF-8 string
            password=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        # Add and commit to the DB session
        db.session.add(user)
        db.session.commit()
        # Return a success message along with the serialized user data
        return jsonify({"message": "User registered successfully!"}, user_schema.dump(user)), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation error
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation error
            # HTTP conflict error
            return {"error": "Email is already registered in the database. Please enter another email."}, 409
    except ValueError as err:
        # Handle the empty password error
        if str(err) == "Password must be non-empty.":
            return {"error": "Password must be non-empty"}, 400


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Manages user login by validating the email and password, 
    generating a JWT token for authenticated users.

    Returns:
        JSON response containing user info and token on successful login.
    Raises:
        404: If the email does not exist.
        401: If the password is invalid.
        400: If required fields are missing.
    """

    body = request.get_json()
    # Convert email address to lowercase to ensure case-insensitivity when comparing email addresses.
    email = body.get("email").strip().lower()

    # check if the email exist
    if email:
        # Create a SQL statement to select the user by email

        # SELECT *
        # FROM User
        # WHERE email = (email);
        statement = db.select(User).filter_by(email=email)
        user = db.session.scalar(statement)

        # Check if the user exists
        if not user:
            return {"error": "the email does NOT exit!"}, 404
    else:
        # Return error if email is missing
        return {"error": "Email is required."}, 400

    password = body.get("password")
    if password:
        # Check if the provided password matches the stored hashed password
        if bcrypt.check_password_hash(user.password, password):
            # Generate a JWT token for the authenticated user
            token = create_access_token(
                # The identity of the token (the user ID in string format)
                identity=str(user.user_id),
                expires_delta=timedelta(days=3))    # The token will expire after 3 days

            # Return the success response with user info and token
            return {"ACCESS GRANTED": {"email": user.email, "is_admin": user.is_admin, "token": token}}
        else:
            # Respond back with an error message if the passeord is invalid
            return {"error": "Invalid password"}, 401   # 401 Unauthorized
    else:
        return {"error": "Password is required"}, 400


@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()     # Ensure the user is authenticated
def update_user():
    """
    Allows authenticated users to update their information.
    Ensures that users can only update their own records.

    Returns:
        JSON response indicating success or failure of the update.
    Raises:
        404: If the user does not exist.
        400: If there are validation errors.
        409: If the email is already registered.
    """

    # Load and validate the incoming JSON data
    body = user_schema_validation.load(request.get_json(), partial=True)
    password = body.get("password")
    # Get the ID of the authenticated user
    user_id = get_jwt_identity()

    # Create a SQL statement to select the user by user_id

    # SELECT *
    # FROM User
    # WHERE user_id = (user_id);
    statement = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(statement)
    # update the user fields if the user is found in the database
    if user:
        try:
            # Update the user's fields with provided data, keeping existing values if not provided
            user.name = body.get("name", "").strip().capitalize() or user.name  #providing a default value to get() in case is None ("")
            user.email = body.get("email", "").strip().lower() or user.email    #providing a default value to get() in case is None ("")

            # If a new password is provided, hash it before saving
            if password:
                user.password = bcrypt.generate_password_hash(
                    password).decode("utf-8")

            # Commit changes to the database
            db.session.commit()
            return jsonify({"message": "User info updated successfully!"}, user_schema.dump(user))
        except IntegrityError as err:
            # Handle specific integrity errors
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                # Handle unique constraint violations
                return {"error": "Email is already registered in the database. Please enter another email."}, 409

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500
    else:
        # Return an error if the user does not exist
        return {"error": f"User {user_id} does NOT exist"}, 404


@auth_bp.route("/", methods=["DELETE"])
@jwt_required()         # Ensure the user is authenticated
def delete_user():
    """
    Securely deletes the current user only if their accounts have a balance of zero.

    Returns:
        JSON response indicating the success or failure of the user deletion.
    Raises:
        400: If there is an active balance in the user's accounts.
        404: If the user does not exist.
    """

    # get authenticated user id
    user_id = get_jwt_identity()

    # Create a SQL statement to check for accounts with a positive balance

    # SELECT *
    # FROM accounts
    # WHERE user_id = (user_id)
    # AND balance > 0;
    statement = db.select(Account).filter(
        Account.user_id == user_id,
        Account.balance > 0)
    account_ids = db.session.scalars(statement)

    if account_ids:
        accounts_details = []
        # Iterate through each account with a positive balance
        for account in account_ids:
            # Create a dictionary for each account
            accounts_details.append(account)
        return {"error": "User cannot be deleted because have accounts liked with a positive balance.",
                "accounts": accounts_schema.dump(accounts_details)}, 400
    else:
        # Create a SQL statement to select the user by user_id

        # SELECT *
        # FROM users
        # WHERE user_id = (user_id);

        statement = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(statement)
        try:
            # Delete the user from the session
            db.session.delete(user)
            # Commit changes to the session
            db.session.commit()
            return {"success": f"The user {user_id} has been succesfully DELETED"}
        except SQLAlchemyError as e:
            # Roll back the session on error
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500
