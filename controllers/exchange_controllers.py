from models.currency import Currency
from models.account import Account
from models.exchange import Exchange, exchange_schema, exchanges_schema
from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.currency_conversion import convert_currency

from flask_jwt_extended import jwt_required, get_jwt_identity

exchange_bp = Blueprint("exchange", __name__, url_prefix="/<int:account_id>/exchanges")

# @exchange_bp.route("/")
# def get_all_exchanges():
#     statement = db.select(Exchange).order_by(Exchange.date_time.asc())
#     exchanges = db.session.scalars(statement)
#     return jsonify(exchanges_schema.dump(exchanges))

@exchange_bp.route("/")
@jwt_required()
def get_exchanges(account_id):
    # Get the user_id from JWT identity
    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    # Check if the account belongs to the user
    # scalar_one_or_none() is used to get a single result or None if no result is found. 
    # This method raises an error if more than one result is found.
    statement = db.select(Account).filter(
        (Account.user_id == user_id) &  #AND operator
        (Account.account_id==account_id)
        )
    account = db.session.scalar(statement)

    if not account:
        return jsonify({'error': 'Account not found for this user'}), 404

    # Get exchanges involving this account
    statement = db.select(Exchange).filter(
            (Exchange.from_account_id == account_id) | #OR opearator
            (Exchange.to_account_id == account_id)
        )
    exchanges = db.session.scalars(statement)

    # Format the results
    return jsonify(exchanges_schema.dump(exchanges))

@exchange_bp.route("/transfer/<int:destination_id>", methods=["POST"])
@jwt_required()
def currency_exchange(account_id, destination_id):
    body = request.get_json()

    if account_id != destination_id:
        statement = db.select(Account).filter_by(account_id=account_id)
        account_from = db.session.scalar(statement)
        if account_from:
            statement = db.select(Account).filter_by(account_id=destination_id)
            account_to = db.session.scalar(statement)
            if not account_to:
                return {"error":"destination account does NOT exist!"}
        else:
            return {"error":"origin account does NOT exist!"}
    else:
        return {"error":"Cannot transfer funds to the same account. Please select a different account."}
    
    # check if both accounts belong to the current user
    current_user = int(get_jwt_identity())
    if account_from.user_id == current_user and account_to.user_id == current_user:
       
       # check 

        if body.get("amount") > 0:
            if account_from.balance >= body.get("amount"):
                account_from.balance -= body.get("amount")
            else:
                return {"error": "Insufficient funds in the origin account."}
        else:
            return {"error":"Amount MUST be greater than 0"}
        
        # get the amount to transfer
        amount = body.get("amount")

        # check if the two accounts have different currency_codes
        # if different currency_code need the conversion
        if account_from.currency_code != account_to.currency_code:
            statement = db.select(Currency).filter_by(currency_code=account_from.currency_code)
            currency_from = db.session.scalar(statement)

            statement = db.select(Currency).filter_by(currency_code=account_to.currency_code)
            currency_to = db.session.scalar(statement)
            amount_exchanged = convert_currency(amount, currency_from.currency_code, currency_to.currency_code)
        else:
            amount_exchanged = amount

        account_to.balance += int(amount_exchanged)

        # create a new instance of Exchange
        new_exchange = Exchange(
            amount = body.get("amount"),
            amount_exchanged = amount_exchanged,
            description = body.get("description"),
            account_origin = account_from,
            account_destination = account_to,
            date_time = datetime.today()
        )

        db.session.add(new_exchange)
        db.session.commit()
        return jsonify(exchange_schema.dump(new_exchange))
    else:
        return {"error":f"The account/s DO NOT belong to the user {current_user}"}
        
