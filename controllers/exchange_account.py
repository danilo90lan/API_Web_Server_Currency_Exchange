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
    statement = db.select(ExchangeAccount).order_by(ExchangeAccount.date_time.desc())
    exchanges = db.session.scalars(statement)
    return jsonify(exchanges_accounts_schema.dump(exchanges))

@ex_acc_bp.route("/", methods=["POST"])
def currency_exchange():
    body = request.get_json()

    statement = db.select(Currency).filter_by(currency=body.get("currency_to"))
    currency_to = db.session.scalar(statement)

    amount_exchanged = body.get("amount")*currency_to.rate

    statement = db.select(Account).filter_by(account_id=body.get("from_account"))
    account_from = db.session.scalar(statement)

    account_from.balance -= body.get("amount")

    statement = db.select(Account).filter_by(account_id=body.get("to_account"))
    account_to = db.session.scalar(statement)

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
        from_account = account_from,
        to_account = account_to,
        exchange = new_exchange
    )


    db.session.add(new_exchange)
    db.session.add(new_exchange_account)
    db.session.commit()


    return {body["currency_to"]:amount_exchanged}


