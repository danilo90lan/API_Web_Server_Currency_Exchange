from models.currency import Currency
from models.account import Account
from models.deposit import Deposit, deposit_schema, deposits_schema
from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity

deposit_bp = Blueprint("deposit", __name__, url_prefix="/<int:account_id>/deposits")

@deposit_bp.route("/")
@jwt_required()
def get_deposits(account_id):
    # Get the user_id from JWT identity
    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    # Check if the account belongs to the user
    statement = db.select(Account).filter(
        (Account.user_id == user_id) &  #AND operator
        (Account.account_id==account_id)
        )
    account = db.session.scalar(statement)

    if not account:
        return jsonify({'error': 'Account not found for this user'}), 404

    # Get deposit involving this account
    statement = db.select(Deposit).filter((Deposit.account_id == account_id))
    exchanges = db.session.scalars(statement)

    # Format the results
    return jsonify(deposits_schema.dump(exchanges))