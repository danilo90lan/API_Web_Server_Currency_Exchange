from flask import current_app
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.account import Account
from models.deposit import Deposit
from models.exchange import Exchange
from models.currency import Currency
from utils.currency import seed_currency_table

from sqlalchemy.exc import SQLAlchemyError


db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    # Initialize currency_table
    seed_currency_table()
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
            name="danilo",
            email="danilo.lann@gmail.com",
            password=bcrypt.generate_password_hash("1234").decode('utf8'),
            is_admin=True
        ),

        User(
            name="alberto",
            email="alberto@gmail.com",
            password=bcrypt.generate_password_hash("1234").decode('utf8'),
            is_admin=True
        ),

        User(
            name="marco",
            email="marco@gmail.com",
            password=bcrypt.generate_password_hash("1234").decode('utf8')
        )
    ]
    
    accounts = [
        Account(
            account_name = "SAVINGS",
            currency_code = "AUD",
            balance = 1000,
            user = users[0]
        ),
            Account(
            account_name = "SAVINGS",
            description = "Buying a new car",
            currency_code = "EUR",
            balance = 3500.76,
            user = users[0]
        ),
            Account(
            account_name = "SAVINGS",
            currency_code = "USD",
            balance = 597,
            user = users[1]
        ),
            Account(
            account_name = "SAVINGS",
            currency_code = "USD",
            balance = 300,
            user = users[2]
        )
    ]

    deposits = [
        Deposit(
            amount = 200,
            description = "Savings",
            account = accounts[1]
        ),
        Deposit(
            amount = 1050,
            description = "car",
            account = accounts[2]
        ),
        Deposit(
            amount = 200,
            description = "Savings",
            account = accounts[0]
        ),
        Deposit(
            amount = 200,
            description = "Savings",
            account = accounts[1]
        )
    ]


    db.session.add_all(deposits)
    db.session.add_all(users)
    print("Users added succesfully")
    db.session.add_all(accounts)
    print("Accounts added succesfully")
    
    try:
        db.session.commit()
        print("Tables seeded!")
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500
