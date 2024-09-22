from models.account import Account
from models.deposit import Deposit, deposit_schema, deposits_schema
from init import db
from flask import Blueprint, request, jsonify

from utils.authorization import check_account_user

from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import ValidationError


deposit_bp = Blueprint("deposit", __name__, url_prefix="/<int:account_id>")

@deposit_bp.route("/deposit-history")
@jwt_required()
@check_account_user
def get_deposits(account_id):
    try:
        statement = db.select(Deposit).filter((Deposit.account_id == account_id)).order_by(Deposit.date_time.desc())
        result = db.session.execute(statement)
        deposits = result.scalars().all()  # Convert to a list in order to check if the list is empty

        if deposits:
            return jsonify(deposits_schema.dump(deposits))
        else:
            return {"message":f"There is NO deposit operations history for the account {account_id}"}
    
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {e}"}, 500 


@deposit_bp.route("/deposit", methods=["POST"])
@jwt_required()
@check_account_user
def deposit_amount(account_id):
    try:
        # Get the deposit amount from the request body
        body = deposit_schema.load(request.get_json())
        amount = body.get("amount")
        
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
        
        db.session.commit()
        # Return the newly created deposit
        return jsonify(deposit_schema.dump(new_deposit)), 201
    
    except ValidationError as ve:
        return {"error": f"Invalid input: {ve.messages}"}, 400 
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500