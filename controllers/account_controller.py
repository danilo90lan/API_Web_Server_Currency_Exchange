# Import Account model and schemas for serialization
from models.account import Account, accounts_schema, account_schema
# Import Currency model
from models.currency import Currency

# Import SQLAlchemy exceptions for error handling
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# Import error codes from psycopg2 for PostgreSQL
from psycopg2 import errorcodes
# Import Forbidden exception for access control
from werkzeug.exceptions import Forbidden

from init import db
# Import Flask modules for routing and JSON responses
from flask import Blueprint, request, jsonify
# Import JWT functions for authentication
from flask_jwt_extended import jwt_required, get_jwt_identity
# Import exchange-related routes
from controllers.exchange_controllers import exchange_bp
# Import deposit-related routes
from controllers.deposit_controller import deposit_bp

# Import utility for checking account ownership
from utils.authorization import check_account_user
# Import utility for admin authorizatio
from utils.authorization import authorize_as_admin

# Create a Blueprint for account routes
account_bp = Blueprint("accounts", __name__, url_prefix="/accounts")
# Register blueprints for exchange and deposit operations
account_bp.register_blueprint(exchange_bp)
account_bp.register_blueprint(deposit_bp)


# Route to get the count of all accounts grouped by user
@account_bp.route("/all")
@jwt_required()     # Ensure the user is authenticated
def count_accounts_grouped_by_currency():
    """
    Retrieves and counts all accounts, providing the counts grouped by currency_code, 
    but only if the requester has admin privileges.

    Returns:
        JSON response containing the count of accounts grouped by currency.
    Raises:
        Forbidden: If the user does not have admin privileges.
    """

    # Check if the user is an admin
    if authorize_as_admin():

        # Query to count accounts and group by currency

        # SELECT currencies.currency_code, COUNT(accounts.account_id)
        # FROM accounts
        # JOIN currencies ON accounts.currency_code = currencies.currency_code
        # GROUP BY currencies.currency_code;
        statement = db.session.query(
            Currency.currency_code, db.func.count(Account.account_id)
        ).join(Currency, Account.currency_code == Currency.currency_code).group_by(Currency.currency_code)

        # Execute the query
        currency_accounts = statement.all()

        # Format the result as a list of dictionaries
        result = []
        for currency, count in currency_accounts:
            record = {
                "Currency": currency,
                "Number of accounts": count
            }
            result.append(record)

        # Return the formatted result as JSON
        return jsonify(result)
    else:
        # Raise a forbidden error if not authorized
        raise Forbidden("You do not have permission to access this resource.")


# get accounts that belong to the current user
@account_bp.route("/")
@jwt_required()         # Ensure the user is authenticated
def get_accounts():
    """
    Retrieves and returns all accounts associated with the authenticated user.

    Returns:
        JSON response containing all accounts for the authenticated user.
    """

    # Query to get all accounts for the authenticated user

    # SELECT *
    # FROM Account
    # WHERE user_id = (user_id);
    statement = db.select(Account).filter_by(user_id=get_jwt_identity())
    accounts = db.session.scalars(statement)
    return jsonify(accounts_schema.dump(accounts))


# get a specific account info
@account_bp.route("/<int:account_id>")
@jwt_required()         # Ensure the user is authenticated
@check_account_user     # Verify the account belongs to the current user
def get_account(account_id):
    """
    Retrieves and returns the details of a specific account identified by the parameter account_id,
    but only if the authenticated user is authorized to access that specific account. 

    Parameters:
        account_id (int): The ID of the account to retrieve.

    Returns:
        JSON response containing the details of the specified account.
    Raises:
        404: If the account is not found.
    """

    # Query to get the specific account by account_id

    # SELECT *
    # FROM Account
    # WHERE account_id = (account_id);
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)
    return jsonify(account_schema.dump(account))


# Adding a new account
@account_bp.route("/", methods=["POST"])
@jwt_required()         # Ensure the user is authenticated
def create_account():
    """
    Creates a new account for the authenticated user based on the data provided 
    in the request body. It ensures that any required fields are provided and returns the responses.

    Returns:
        JSON response indicating the success or failure of the account creation.
    Raises:
        IntegrityError: If required fields are missing or if there are database integrity issues.
    """

    # Load and validate the incoming JSON data
    body = account_schema.load(request.get_json())

    try:
        # Create a new Account object
        account = Account(
            # Capitalize the account name
            account_name=body.get("account_name").capitalize(),
            balance=body.get("balance"),
            currency_code=body.get("currency_code"),
            # Get the user ID from the JWT token
            user_id=int(get_jwt_identity())
        )
        # Add the new account to the database session
        db.session.add(account)

        try:
            # Commit the transactio to the session
            db.session.commit()
            return jsonify({"SUCCESS": account_schema.dump(account)}), 201
        except SQLAlchemyError as e:
            # Rollback the session if there's a database error
            db.session.rollback()
            # Return an error response for the database operation failure
            return {"error": f"Database operation failed {e}"}, 500
    except IntegrityError as err:
        # Handle integrity errors, such as NOT NULL violations
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        else:
            return {"error": "Database integrity error"}, 500


@account_bp.route("/<int:account_id>", methods=["PATCH"])
@jwt_required()     # Ensure the user is authenticated
@check_account_user     # Verify the account belongs to the current user
def update_account(account_id):
    """
    Allows for the partial updating of specified account details 
    while ensuring that the user has permission to make changes.

    Parameters:
        account_id (int): The ID of the account to update.

    Returns:
        JSON response indicating the success or failure of the account update.
    Raises:
        404: If the account does not exist.
    """

    # Query to get the specific account by account_id

    # SELECT *
    # FROM Account
    # WHERE account_id = (account_id);
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)

    # Check if the account exists
    if account:
        # Load and validate the incoming JSON data for partial updates
        body = account_schema.load(request.get_json(), partial=True)
        # Update account fields with new values, keeping existing ones if not provided
        account.account_name = body.get("account_name") or account.account_name
        try:
            # Commit the changes
            db.session.commit()
            return jsonify({"message": "Account info updated successfully!"}, account_schema.dump(account))
        except SQLAlchemyError as e:
            # Rollback the session if there's a database error
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500
    else:
        # Return an error if the account does not exist
        return {"error": f"Account {account_id} does NOT exist!"}


@account_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()         # Ensure the user is authenticated
@check_account_user     # Verify the account belongs to the current user
def delete_Account(account_id):
    """
    Securely deletes a specified account only if the balance is zero.

    Parameters:
        account_id (int): The ID of the account to delete.

    Returns:
        JSON response indicating the success or failure of the account deletion.
    Raises:
        400: If there is an active balance in the account.
    """

    # Query to get the specific account by account_id

    # SELECT *
    # FROM Account
    # WHERE account_id = (account_id);
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)

    # Check if the account balance is zero
    if account.balance == 0:
        # Delete the account from the session
        db.session.delete(account)
        try:
            # commit to the session
            db.session.commit()
            return {"success": f"The account {account_id} has been succesfully DELETED"}
        except SQLAlchemyError as e:
            # Rollback if there's a database error
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500

    else:
        return {"error": f"There is ACTIVE balance in the account {account_id}. Please transfer the remaining balance before closing the account!"}, 400
