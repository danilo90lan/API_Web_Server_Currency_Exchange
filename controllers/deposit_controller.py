from models.account import Account
from models.deposit import Deposit, deposit_schema, deposits_schema
from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity

deposit_bp = Blueprint("deposit", __name__, url_prefix="/<int:account_id>")

@deposit_bp.route("/deposit-history")
@jwt_required()
def get_deposits(account_id):
    # Get the user_id from JWT identity
    user_id = get_jwt_identity()
    # Check if the account belongs to the user
    statement = db.select(Account).filter(
        (Account.user_id == user_id) &  #AND operator
        (Account.account_id==account_id)
        )
    account = db.session.scalar(statement)

    if not account:
        return jsonify({"error": "This account doesn NOT belong to the current user"}), 404

    # Get deposit involving this account
    statement = db.select(Deposit).filter((Deposit.account_id == account_id))
    deposits = db.session.scalars(statement)

    if deposits==None:
        return jsonify(deposits_schema.dump(deposits))
    else:
        return {"message":f"There is NO deposit operations hsistory for the account {account_id}"}

@deposit_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit_amount(account_id):
    # Get the user_id from JWT identity
    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Check if the account belongs to the user
    statement = db.select(Account).filter(
        (Account.user_id == user_id) &
        (Account.account_id == account_id)
    )
    account = db.session.scalar(statement)

    if not account:
        return jsonify({"error": "This account doesn NOT belong to the current user"}), 404

    # Get the deposit amount from the request body
    body = request.get_json()
    amount = body.get('amount')
    
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    # update account's balance
    account.balance += amount

    # Create a new deposit record
    new_deposit = Deposit(
        amount = amount,
        date_time = datetime.now(),
        account = account
    )
    db.session.add(new_deposit)
    db.session.commit()

    # Return the newly created deposit
    return jsonify(deposit_schema.dump(new_deposit)), 201