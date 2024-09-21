from init import db
import requests
from requests.exceptions import HTTPError, Timeout, RequestException

from models.currency import Currency
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

def get_currencies():
    endpoint = "https://openexchangerates.org/api/latest.json?app_id=e73026dfbc164a59a8fb416cc067ca33"
    try:
        response = requests.get(endpoint)
        # raise an exception if a 400 or 500 error occurs
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        return f"HTTP error occurred: {http_err}", 500
    except Timeout:
        return "The request timed out", 408         # 408 is the HTTP status code for Request Timeout
    except RequestException as req_err:
        return f"Request failed: {req_err}", 500
    

def seed_currency_table():
    list_currency = []
    currency = get_currencies()
    # Prepare the values for insertion as Currency objects
    for code, rate in currency["rates"].items():
        currency_obj = Currency(
            currency_code=code,
            rate=rate,
            base_code=currency["base"]
        )
        list_currency.append(currency_obj)

    # Add all Currency objects to the session
    db.session.add_all(list_currency)
    try:
        db.session.commit()
        print("Currencies seeded successfully!")
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500


def update_exchange_rates(app):
    with app.app_context():
        currency = get_currencies()
        try:
            # Loop through the currency data and update the corresponding rows
            for code, rate in currency["rates"].items():
                # Update only the existing records
                db.session.query(Currency).filter_by(currency_code=code).update({
                    "rate": rate,
                    "last_update": func.now()
                })
            db.session.commit()
            print("Currencies updated successfully!")
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500


def get_currencies_codes():
    currency = get_currencies()
    list_currency_codes = currency["rates"].keys()
    return tuple(list_currency_codes)