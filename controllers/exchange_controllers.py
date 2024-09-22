from models.currency import Currency
from models.account import Account
from models.exchange import Exchange, exchange_schema, exchanges_schema
from init import db
from flask import Blueprint, request, jsonify

from utils.authorization import check_account_user
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import ValidationError


exchange_bp = Blueprint("exchange", __name__, url_prefix="/<int:account_id>")


@exchange_bp.route("/exchange-history")
@jwt_required()
@check_account_user
def get_exchanges(account_id):
    """
    Retrieves the exchange history for the specified account.
    
    This function returns a list of exchange records involving the account,
    regardless of whether the account is the sender or the receiver.
    """
    try:
        # SELECT *
        # FROM Exchange
        # WHERE from_account_id = (account_id) OR to_account_id = (account_id)
        # ORDER BY date_time DESC;
        statement = db.select(Exchange).filter(
                (Exchange.from_account_id == account_id) | #OR opearator
                (Exchange.to_account_id == account_id)
            ).order_by(Exchange.date_time.desc())  # Order by date_time in descending order
        
        result = db.session.execute(statement)
        exchanges = result.scalars().all() 

        if exchanges:
            return jsonify(exchanges_schema.dump(exchanges))
        else:
            return {"message":f"There is NO exchanges operations history for the account {account_id}"}
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {e}"}, 500 


@exchange_bp.route("/transfer/<int:destination_id>", methods=["POST"])
@jwt_required()
@check_account_user # Verify the account that initiate the transfer belongs to the current user
def currency_exchange(account_id, destination_id):
    """
    Transfers funds from the source account to the destination account.
    The destination account can belong to any user
    If the source and destination accounts have different currency codes,
    the function converts the amount based on the current exchange rates.
    """

    # Check if the source and destination accounts are the same
    if account_id == destination_id:
        return {"error":"Cannot transfer funds to the same account. Please select a different account."}
    
    # Load the request body and extract the amount
    # the amount has been already validated (amount > 0)
    body = exchange_schema.load(request.get_json())
    amount = body.get("amount")
    
    try:
        # SELECT * FROM Account WHERE account_id = (account_id);
        statement = db.select(Account).filter_by(account_id=account_id)
        account_from = db.session.scalar(statement)

        # Check if the source account has sufficient funds
        if account_from.balance >= amount:
            account_from.balance = float(account_from.balance) - amount
        else:
            return {"error": f"Insufficient funds in the account {account_from.account_id}."}

        # check if the two accounts have different currency_codes
        # if different currency_code needs the currency conversion to be performed

        # SELECT * FROM Account WHERE account_id = :destination_id;
        statement = db.select(Account).filter_by(account_id=destination_id)
        account_to = db.session.scalar(statement)

        # Check if the two accounts have different currency codes
        if account_from.currency_code != account_to.currency_code:

            # SELECT * FROM Currency WHERE currency_code = (currency_code);
            statement = db.select(Currency).filter_by(currency_code=account_from.currency_code)
            currency_from = db.session.scalar(statement)

            # SELECT * FROM Currency WHERE currency_code = (currency_code);
            statement = db.select(Currency).filter_by(currency_code=account_to.currency_code)
            currency_to = db.session.scalar(statement)

            # Convert the amount based on the current exchange rates
            amount_exchanged = (amount / currency_from.rate) * currency_to.rate
        else:
            # If the currency codes are the same, no conversion is needed
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
        # Add the new exchange record to the session
        db.session.add(new_exchange)
        # Commit the transaction to the database
        db.session.commit()
        return jsonify(exchange_schema.dump(new_exchange))
    except ValidationError as ve:
        # Handle validation errors for the request data
        return {"error": f"Invalid input: {ve.messages}"}, 400
    except SQLAlchemyError as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500    
