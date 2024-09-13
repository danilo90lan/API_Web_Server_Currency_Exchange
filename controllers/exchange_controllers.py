from models.currency import Currency
from models.account import Account
from models.exchange import Exchange, exchange_schema, exchanges_schema
from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.currency_conversion import convert_currency

exchange_bp = Blueprint("ex_acc", __name__, url_prefix="/exchange")

@exchange_bp.route("/")
def get_all_exchanges():
    statement = db.select(Exchange).order_by(Exchange.date_time.asc())
    exchanges = db.session.scalars(statement)
    return jsonify(exchanges_schema.dump(exchanges))

@exchange_bp.route("/<int:origin_id>/transfer/<int:destination_id>", methods=["POST"])
def currency_exchange(origin_id, destination_id):
    body = request.get_json()

    if origin_id != destination_id:

        statement = db.select(Account).filter_by(account_id=origin_id)
        account_from = db.session.scalar(statement)

        statement = db.select(Account).filter_by(account_id=destination_id)
        account_to = db.session.scalar(statement)
    else:
        return {"error":"Cannot transfer funds to the same account. Please select a different account."}

    if not account_from:
        return {"error":"origin account does NOT exist!"}

    if not account_to:
        return {"error":"origin account does NOT exist!"}
       
    if account_from.currency_code != body.get("currency_from"):
        return {"error":f"origin account has a different currency! ({account_from.currency_code})"}

    if account_to.currency_code != body.get("currency_to"):
        return {"error":f"destination account has a different currency! ({account_to.currency_code})"}

    account_from.balance -= body.get("amount")

    statement = db.select(Currency).filter_by(currency_code=body.get("currency_from"))
    currency_from = db.session.scalar(statement)

    statement = db.select(Currency).filter_by(currency_code=body.get("currency_to"))
    currency_to = db.session.scalar(statement)

    amount = body.get("amount")
    amount_exchanged = convert_currency(amount, currency_from.currency_code, currency_to.currency_code)
    account_to.balance += int(amount_exchanged)

    db.session.commit()

    new_exchange = Exchange(
        amount = body.get("amount"),
        currency_from = body.get("currency_from"),
        amount_exchanged = amount_exchanged,
        currency_to = body.get("currency_to"),
        description = body.get("description"),
        account_origin = account_from,
        account_destination = account_to,
        date_time = datetime.today()
    )


    db.session.add(new_exchange)
    db.session.commit()


    return {body["currency_to"]:amount_exchanged}
