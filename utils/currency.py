from init import db
from models.currency import Currency
import requests
from sqlalchemy import func

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
    for i, j in currency["conversion_rates"].items():
        currency_obj = Currency(
            currency_code=i,
            rate=j,
            base_code=currency["base_code"]
        )
        list_currency.append(currency_obj)

    # Add all Currency objects to the session
    try:
        db.session.add_all(list_currency)
        db.session.commit()
        print("Currencies seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding currencies: {e}")

def update_exchange_rates(app):
    with app.app_context():
        currency = get_currencies()
        try:
            # Loop through the currency data and update the corresponding rows
            for code, rate in currency["conversion_rates"].items():
                # Update only the existing records
                db.session.query(Currency).filter_by(currency_code=code).update({
                    "rate": rate,
                    "last_update": func.now()
                })
            db.session.commit()
            print("Currencies updated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating currencies: {e}")

def get_currencies_codes():
    currency = get_currencies()
    list_currency_codes = []
    for i in currency["conversion_rates"].items():
        code = i[0]
        list_currency_codes.append(code)
    return tuple(list_currency_codes)
