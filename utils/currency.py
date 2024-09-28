from init import db
import requests
from requests.exceptions import HTTPError, Timeout, RequestException

from models.currency import Currency
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError


def get_currencies():
    """
    Retrieve currency data from an external API.

    Returns:
        dict: The JSON response containing currency data.

    Raises:
        500: If an HTTP error occurs during the request.
        408: If the request times out.
    """

    endpoint = "https://openexchangerates.org/api/latest.json?app_id=71562a44ff3d4ad98578bb6d44ef9a9b"
    try:
        # Make a GET request to the API endpoint
        response = requests.get(endpoint)
        # raise an exception if a 400 or 500 error occurs
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        # Handle HTTP errors
        return f"HTTP error occurred: {http_err}", 500
    except Timeout:
        # Handle request timeouts
        # 408 is the HTTP status code for Request Timeout
        return "The request timed out", 408
    except RequestException as req_err:
        # Handle other request-related exceptions
        return f"Request failed: {req_err}", 500


def seed_currency_table():
    """
    Seed the currency data into the database by retrieving it from an external API.

    Returns:
        dict: A success message or an error message in case of failure.

    Raises:
        500: If a database operation fails.
    """

    list_currency = []

    # Fetch currency data from the external API
    currency = get_currencies()

    # Create Currency objects retrieving the rates and the currency_code
    # from the third-party API response (JSON object) and append it to list_currency
    for code, rate in currency["rates"].items():
        currency_obj = Currency(
            currency_code=code,
            rate=rate,
            base_code=currency["base"]
        )
        # Append the newly created Currency object to the list
        list_currency.append(currency_obj)

    # Add all Currency objects to the session
    db.session.add_all(list_currency)
    try:
        db.session.commit()
        print("Currencies initialized successfully!")
    except SQLAlchemyError as e:
        # Rollback on error
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500


def update_exchange_rates(app):
    """
    Periodically update exchange rates in the database with new values fetched from the API.
    This function is called by the APScheduler in the background.

    Args:
        app: The Flask application context.

    Returns:
        dict: A success message or an error message in case of failure.

    Raises:
        500: If a database operation fails.
    """

    # Create an application context so the function can access Flask resources like the database
    with app.app_context():
        # Retrieve the latest currency data from the external API
        currency = get_currencies()

        try:
            # Loop through the currency data and update the corresponding rows
            for code, rate in currency["rates"].items():

                # Update only the existing records
                # UPDATE Currency
                # SET rate = (new_rate), last_update = (datetime.now()
                # WHERE currency_code = '(currency_code)'
                db.session.query(Currency).filter_by(currency_code=code).update({
                    "rate": rate,               # Set the new exchange rate
                    "last_update": func.now()   # Update the last_update timestamp
                })

            # Commit the transaction to save changes
            db.session.commit()
            print("Currencies updated successfully!")
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database operation failed {e}"}, 500


def get_currencies_codes():
    """
    Retrieve currency codes from the currency JSON object obtained from the third-party API.

    Returns:
        tuple: A tuple containing all the currency codes.

    Raises:
        500: If there is an error retrieving currency data.
    """

    currency = get_currencies()
    list_currency_codes = currency["rates"].keys()
    return tuple(list_currency_codes)
