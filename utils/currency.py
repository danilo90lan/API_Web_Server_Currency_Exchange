from init import db
import requests
from models.currency import Currency
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

def get_currencies():
    endpoint = "https://v6.exchangerate-api.com/v6/b12835ecd29b6518d756378d/latest/USD"
    response = requests.get(endpoint)
    if response.ok:
        return response.json()
    else:
        return "The request failed", response.status_code
    
def seed_currency_table():
    list_currency = []
    currency = get_currencies()
    # Prepare the values for insertion as Currency objects
    for code, rate in currency["conversion_rates"].items():
        currency_obj = Currency(
            currency_code=code,
            rate=rate,
            base_code=currency["base_code"]
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
        # Loop through the currency data and update the corresponding rows
        for code, rate in currency["conversion_rates"].items():
            # Update only the existing records
            db.session.query(Currency).filter_by(currency_code=code).update({
                "rate": rate,
                "last_update": func.now()
            })
        try:
            db.session.commit()
            print("Currencies updated successfully!")
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500

def get_currencies_codes():
    currency = get_currencies()
    list_currency_codes = []
    for i in currency["conversion_rates"].items():
        code = i[0]
        list_currency_codes.append(code)
    return tuple(list_currency_codes)
