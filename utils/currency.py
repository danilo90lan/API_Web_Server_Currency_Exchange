from init import db
from models.currency import Currency
from datetime import datetime
import requests


def get_currencies():
    endpoint = "https://v6.exchangerate-api.com/v6/b12835ecd29b6518d756378d/latest/USD"
    response = requests.get(endpoint)
    if response.ok:
        return response.json()
    else:
        return "The request failed", response.status_code


def update_exchange_rates():
    list_currency = []
    currency = get_currencies()
    updated_date = currency["time_last_update_utc"]  
    try:
        # Convert the string to a datetime object
        last_update_dt = datetime.strptime(updated_date, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError as e:
        print("Error parsing date:", e) 

    # Format the datetime object to get just the date
    last_update_date = last_update_dt.strftime("%Y-%m-%d")

    for i, j in currency["conversion_rates"].items():
        value = Currency(
            currency_code = i,
            rate = j,
            base_code = currency["base_code"],
            last_update = last_update_date
        )
        list_currency.append(value)
        
    db.session.add_all(list_currency)
    db.session.commit()
    print("Currencies added succesfully!")
   