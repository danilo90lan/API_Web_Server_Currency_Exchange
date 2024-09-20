from models.account import Account
from models.deposit import Deposit, deposit_schema, deposits_schema
from init import db
from flask import Blueprint, request, jsonify

from utils.authorization import check_account_user

from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

deposit_bp = Blueprint("deposit", __name__, url_prefix="/<int:account_id>")

@deposit_bp.route("/deposit-history")
@jwt_required()
def get_deposits(account_id):
    verify_account = check_account_user(account_id)
    if verify_account == True:

        # Get deposit involving this account
        statement = db.select(Deposit).filter((Deposit.account_id == account_id))
        result = db.session.execute(statement)
        deposits = result.scalars().all()  # Convert to a list in order to check if the list is empty

        if deposits:
            return jsonify(deposits_schema.dump(deposits))
        else:
            return {"message":f"There is NO deposit operations history for the account {account_id}"}
    else:
        return verify_account

@deposit_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit_amount(account_id):
    verify_account = check_account_user(account_id)
    if verify_account == True:

        # Get the deposit amount from the request body
        body = deposit_schema.load(request.get_json())
        amount = body.get('amount')
        
        # get the account
        statement = db.select(Account).filter_by(account_id=account_id)
        account = db.session.scalar(statement)

        # update account's balance
        account.balance = float(account.balance) + amount

        # Create a new deposit record
        new_deposit = Deposit(
            amount = amount,
            description = body.get("description"),
            account = account
        )
        db.session.add(new_deposit)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500

        # Return the newly created deposit
        return jsonify(deposit_schema.dump(new_deposit)), 201
    else:
        return verify_account