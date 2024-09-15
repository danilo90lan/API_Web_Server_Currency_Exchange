from models.currency import Currency
from models.account import Account
from models.exchange import Exchange, exchange_schema, exchanges_schema
from init import db
from flask import Blueprint, request, jsonify

from utils.check_account_user import check_account_user

from flask_jwt_extended import jwt_required, get_jwt_identity

exchange_bp = Blueprint("exchange", __name__, url_prefix="/<int:account_id>")

# @exchange_bp.route("/")
# def get_all_exchanges():
#     statement = db.select(Exchange).order_by(Exchange.date_time.asc())
#     exchanges = db.session.scalars(statement)
#     return jsonify(exchanges_schema.dump(exchanges))

@exchange_bp.route("/exchange-history")
@jwt_required()
def get_exchanges(account_id):
    verify_account = check_account_user(account_id)
    if verify_account==True:

        # Get exchanges involving this account
        statement = db.select(Exchange).filter(
                (Exchange.from_account_id == account_id) | #OR opearator
                (Exchange.to_account_id == account_id)
            )
        result = db.session.execute(statement)
        exchanges = result.scalars().all()  # Convert to a list in order to check if the list is empty

        if exchanges:
            return jsonify(exchanges_schema.dump(exchanges))
        else:
            return {"message":f"There is NO exchanges operations history for the account {account_id}"}
    else:
        return verify_account 


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
            # convertimg the rates from Currency A to currency B
            amount_exchanged = (amount / currency_from.rate) * currency_to.rate
        else:
            amount_exchanged = amount

        account_to.balance = float(account_to.balance) + amount_exchanged

        # create a new instance of Exchange
        new_exchange = Exchange(
            amount = body.get("amount"),
            amount_exchanged = amount_exchanged,
            description = body.get("description"),
            account_origin = account_from,
            account_destination = account_to
        )

        db.session.add(new_exchange)
        db.session.commit()
        return jsonify(exchange_schema.dump(new_exchange))
    else:
        return {"error":f"The account/s DO NOT belong to the user {current_user}"}
        
