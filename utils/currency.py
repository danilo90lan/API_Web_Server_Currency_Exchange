from init import db
from models.currency import Currency
import requests
from sqlalchemy.dialects.postgresql import insert

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
        list_currency = []
        currency = get_currencies()

        # Prepare the values for insertion
        for i, j in currency["conversion_rates"].items():
            list_currency.append({
                'currency_code': i,
                'rate': j,
                'base_code': currency["base_code"]
            })

        # Create an upsert statement
        stmt = insert(Currency).values(list_currency)
        stmt = stmt.on_conflict_do_update(
            index_elements=['currency_code'],
            set_={
                'rate': stmt.excluded.rate,
                'last_update': stmt.excluded.last_update
            }
        )

        # Execute the statement
        try:
            db.session.execute(stmt)
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
