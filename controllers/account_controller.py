from models.account import Account, accounts_schema, account_schema
from models.user import User

from init import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.exchange_controllers import exchange_bp
from controllers.deposit_controller import deposit_bp
from datetime import datetime

from utils.check_account_user import check_account_user
from utils.check_admin import authorize_as_admin


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
                "number of active accounts": count
            }
            result.append(record)
        return jsonify(result)
    else:
        return {"error": "Not authorized to perform this action!"}

# get accounts that belong to the id
@account_bp.route("/")
@jwt_required()
def get_accounts():
    statement = db.select(Account).filter_by(user_id=get_jwt_identity())
    accounts = db.session.scalars(statement)
    return accounts_schema.dump(accounts)

# Adding a new account
@account_bp.route("/", methods=["POST"])
@jwt_required()
def create_account():
    body = request.get_json()
    account = Account(
        balance = body.get("balance"),
        currency_code = body.get("currency_code"),
        date_creation = datetime.today(),
        user_id = int(get_jwt_identity())
    )
    db.session.add(account)
    db.session.commit()
    return {"SUCCESS":account_schema.dump(account)}

@account_bp.route("/<int:account_id>", methods=["PATCH"])
@jwt_required()
def update_account(account_id):
    verify_account = check_account_user(account_id)
    if verify_account == True:
        statement = db.select(Account).filter_by(account_id=account_id)
        account = db.session.scalar(statement)
        if account:
            body = request.get_json()
            account.account_name = body.get("account_name") or account.account_name
            account.description = body.get("description") or account.description

            db.session.commit()
            return jsonify({"message": "Account info updated successfully!"}, account_schema.dump(account))
        else:
            return verify_account



@account_bp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_Account(account_id):
    verify_account = check_account_user(account_id)
    if verify_account == True:
        statement = db.select(Account).filter_by(account_id=account_id)
        account = db.session.scalar(statement)
        
        if account.balance == 0:
            db.session.delete(account)
            db.session.commit()
            return {"success":f"The account {account_id} has been succesfully DELETED"}
        else:
            return {"error":f"There is ACTIVE balance in the account {account_id}. Please transfer the remaining balance before closing the account!"}
    else:
        return verify_account