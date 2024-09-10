from models.exchange_account import ExchangeAccount, exchange_account_schema, exchanges_accounts_schema
from models.currency import Currency
from models.account import Account
from models.exchange import Exchange
from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime

ex_acc_bp = Blueprint("ex_acc", __name__, url_prefix="/exchanges")

@ex_acc_bp.route("/")
def get_all_exchanges():
    statement = db.select(ExchangeAccount).order_by(ExchangeAccount.date_time.asc())
    exchanges = db.session.scalars(statement)
    return jsonify(exchanges_accounts_schema.dump(exchanges))

@ex_acc_bp.route("/", methods=["POST"])
def currency_exchange():
    body = request.get_json()

    statement = db.select(Account).filter_by(account_id=body.get("from_account"))
    account_from = db.session.scalar(statement)

    statement = db.select(Account).filter_by(account_id=body.get("to_account"))
    account_to = db.session.scalar(statement)

    if not account_from:
        return {"error":"the origin account doesn't exist!"}
    
    if not account_to:
        return {"error":"the destination account doesn't exist!"}
    
    if account_from.currency != body.get("currency_from"):
        return {"error":f"origin account has a different currency! ({account_from.currency})"}

    if account_to.currency != body.get("currency_to"):
        return {"error":f"destination account has a different currency! ({account_to.currency})"}

    account_from.balance -= body.get("amount")

    statement = db.select(Currency).filter_by(currency=body.get("currency_from"))
    currency_from = db.session.scalar(statement)

    statement = db.select(Currency).filter_by(currency=body.get("currency_to"))
    currency_to = db.session.scalar(statement)

    amount = body.get("amount")
    amount_exchanged = convert_currency(amount, currency_from.currency, currency_to.currency)
    account_to.balance += int(amount_exchanged)

    db.session.commit()

    new_exchange = Exchange(
        amount = body.get("amount"),
        currency_from = body.get("currency_from"),
        amount_exchanged = amount_exchanged,
        currency_to = body.get("currency_to"),
        description = body.get("description")
    )

    new_exchange_account = ExchangeAccount(
        date_time = datetime.today(),
        account_origin = account_from,
        account_destination = account_to,
        exchange = new_exchange
    )


    db.session.add(new_exchange)
    db.session.add(new_exchange_account)
    db.session.commit()


    return {body["currency_to"]:amount_exchanged}

def convert_currency(amount, origin, destination):
    """
Convert an amount from Currency A to Currency B using USD as the base.

"""
    
    statement = db.select(Currency).filter_by(currency=origin)
    from_code = db.session.scalar(statement)
    statement = db.select(Currency).filter_by(currency=destination)
    to_code = db.session.scalar(statement)

    conversion = (amount / from_code.rate) * to_code.rate
    return conversion