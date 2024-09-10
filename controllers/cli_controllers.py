from flask import current_app
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.account import Account
from models.operation import Operation
from models.exchange import Exchange
from models.exchange_account import ExchangeAccount
from models.currency import Currency
from datetime import datetime
from sqlalchemy import text
import requests


db_commands = Blueprint("db", __name__)

def get_currencies():
    endpoint = "https://v6.exchangerate-api.com/v6/b12835ecd29b6518d756378d/latest/USD"
    response = requests.get(endpoint)
    if response.ok:
        return response.json()
    else:
        return "The request  failed", response.status_code

def update_currency():
    list_currency = []
    currency = get_currencies()
    updated_date = currency["time_last_update_utc"]  
    try:
        # Convert the string to a datetime object
        last_update_dt = datetime.strptime(updated_date, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError as e:
        print("Error parsing date:", e)  # Debug: print any parsing errors

    # Format the datetime object to get just the date
    last_update_date = last_update_dt.strftime("%Y-%m-%d")

    for i in currency["conversion_rates"].items():
        value = Currency(
            currency = i[0],
            rate = i[1],
            base_code = currency["base_code"],
            last_update = last_update_date
        )
        list_currency.append(value)
        
    db.session.add_all(list_currency)
    print("Currencies added succesfully!")
   

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_tables():
        # Connect to the database
        with current_app.app_context():
            db.reflect()  # Reflect the current database structure
            db.drop_all()  # This will drop all tables
            print("All tables dropped successfully")

@db_commands.cli.command("seed")
def seed_database():
    
    users = [
        User(
            name="User 1",
            email="cao@gmail.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
            is_admin=True
        ),

        User(
            name="User 2",
            email="alberto@gmail.com",
            password=bcrypt.generate_password_hash("5678").decode('utf8'),
            is_admin=True
        ),

        User(
            name="User 3",
            email="marco@gmail.com",
            password=bcrypt.generate_password_hash("10998765").decode('utf8')
        )
    ]
    
    accounts = [
        Account(
            currency = "AUD",
            balance = 1000,
            date_creation = datetime.now(),
            user = users[0]
        ),
            Account(
            currency = "EUR",
            balance = 3500.76,
            date_creation = datetime.now(),
            user = users[0]
        ),
            Account(
            currency = "USD",
            balance = 597,
            date_creation = datetime.now(),
            user = users[1]
        ),
            Account(
            currency = "USD",
            balance = 300,
            date_creation = datetime.now(),
            user = users[2]
        )
    ]

    operations = [
        Operation(
            operation_type = "deposit",
            currency = "EUR",
            amount = 200,
            description = "Savings",
            date = datetime.now(),
            account = accounts[1]
        ),
        Operation(
            operation_type = "deposit",
            currency = "USD",
            amount = 1050,
            description = "car",
            date = datetime.now(),
            account = accounts[2]
        ),
        Operation(
            operation_type = "withdraw",
            currency = "AUD",
            amount = 200,
            description = "Savings",
            date = datetime.now(),
            account = accounts[0]
        ),
        Operation(
            operation_type = "deposit",
            currency = "EUR",
            amount = 200,
            description = "Savings",
            date = datetime.now(),
            account = accounts[1]
        )
    ]

    

    update_currency()

    db.session.add_all(operations)
    db.session.add_all(users)
    print("Users added succesfully")
    db.session.add_all(accounts)
    print("Accounts added succesfully")
    
    try:
        db.session.commit()
        print("Tables seeded!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
