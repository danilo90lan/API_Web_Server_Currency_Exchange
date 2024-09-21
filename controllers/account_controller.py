from models.account import Account, accounts_schema, account_schema
from models.user import User

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes
from werkzeug.exceptions import Forbidden

from init import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.exchange_controllers import exchange_bp
from controllers.deposit_controller import deposit_bp

from utils.authorization import check_account_user
from utils.authorization import authorize_as_admin


account_bp = Blueprint("accounts", __name__, url_prefix="/accounts")
account_bp.register_blueprint(exchange_bp)
account_bp.register_blueprint(deposit_bp)


#get all accounts
@account_bp.route("/all")
@jwt_required()
def count_accounts_grouped_by_user():
    if authorize_as_admin():
        # Query to count the accounts, grouped by user_id. Perform a JOIN
        # with the User table in order to retrieve the account name
        statement = db.session.query(
            User.user_id, User.name, db.func.count(Account.account_id)
        ).join(Account, User.user_id == Account.user_id).group_by(User.user_id, User.name)

        user_accounts = statement.all()

        # Format the result
        result = []
        for user_id, name, count in user_accounts:
            record = {
                "user_id": user_id,
                "name": name,
                "number of accounts": count
            }
            result.append(record)
        return jsonify(result)
    else:
        raise Forbidden("You do not have permission to access this resource.")


# get accounts that belong to the current user
@account_bp.route("/")
@jwt_required()
def get_accounts():
    statement = db.select(Account).filter_by(user_id=get_jwt_identity())
    accounts = db.session.scalars(statement)
    return jsonify(accounts_schema.dump(accounts))


# get a specific account info
@account_bp.route("/<int:account_id>")
@jwt_required()
@check_account_user
def get_account(account_id):
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)
    return jsonify(account_schema.dump(account))


# Adding a new account
@account_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    body = account_schema.load(request.get_json())
    try:
        account = Account(
            account_name = body.get("account_name"),
            description = body.get("description"),
            balance = body.get("balance"),
            currency_code = body.get("currency_code"),
            user_id = int(get_jwt_identity())
        )
        db.session.add(account)
        try:
            db.session.commit()
            return jsonify({"SUCCESS":account_schema.dump(account)})
        except SQLAlchemyError as e:
                db.session.rollback()
                return {"error": f"Database operation failed {e}"}, 500
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        else:
            return {"error": "Database integrity error"}, 500

@account_bp.route("/<int:account_id>", methods=["PATCH"])
@jwt_required()
@check_account_user
def update_account(account_id):
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)
    if account:
        body = account_schema.load(request.get_json(), partial=True)
        account.account_name = body.get("account_name") or account.account_name
        account.description = body.get("description") or account.description
        try:
            db.session.commit()
            return jsonify({"message": "Account info updated successfully!"}, account_schema.dump(account))
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500
    else:
        return {"error": f"Account {account_id} does NOT exist!"}

@account_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
@check_account_user
def delete_Account(account_id):
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)
    
    if account.balance == 0:
        db.session.delete(account)
        try:
            db.session.commit()
            return {"success":f"The account {account_id} has been succesfully DELETED"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500

    else:
            return {"error":f"There is ACTIVE balance in the account {account_id}. Please transfer the remaining balance before closing the account!"}