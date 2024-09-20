from models.currency import Currency
from models.account import Account
from models.exchange import Exchange, exchange_schema, exchanges_schema
from init import db
from flask import Blueprint, request, jsonify

from utils.authorization import check_account_user
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError

exchange_bp = Blueprint("exchange", __name__, url_prefix="/<int:account_id>")


@exchange_bp.route("/exchange-history")
@jwt_required()
@check_account_user
def get_exchanges(account_id):
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


@exchange_bp.route("/transfer/<int:destination_id>", methods=["POST"])
@jwt_required()
@check_account_user
def currency_exchange(account_id, destination_id):
    if account_id == destination_id:
        return {"error":"Cannot transfer funds to the same account. Please select a different account."}
    
    # Both accounts have been validated by the `check_account_user` decorator.
    body = exchange_schema.load(request.get_json())
    amount = body.get("amount")
    statement = db.select(Account).filter_by(account_id=account_id)
    account_from = db.session.scalar(statement)
    if account_from.balance >= amount:
        account_from.balance = float(account_from.balance) - amount
    else:
        return {"error": f"Insufficient funds in the account {account_from.account_id}."}


    # check if the two accounts have different currency_codes
    # if different currency_code needs the currency conversion
    statement = db.select(Account).filter_by(account_id=destination_id)
    account_to = db.session.scalar(statement)
    if account_from.currency_code != account_to.currency_code:
        statement = db.select(Currency).filter_by(currency_code=account_from.currency_code)
        currency_from = db.session.scalar(statement)

        statement = db.select(Currency).filter_by(currency_code=account_to.currency_code)
        currency_to = db.session.scalar(statement)

        # converting the rates from Currency A to currency B
        amount_exchanged = (amount / currency_from.rate) * currency_to.rate
    else:
        amount_exchanged = amount

    # update the balance of the destination accont
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
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500
    return jsonify(exchange_schema.dump(new_exchange))
    
