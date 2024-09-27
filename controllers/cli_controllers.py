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
    print("Tables created")
    # Initialize currency_table
    seed_currency_table()


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
            name="Danilo",
            email="danilo@gmail.com",
            password=bcrypt.generate_password_hash("ABCDabcd1").decode('utf8'),
            is_admin=True
        ),

        User(
            name="Alberto",
            email="alberto@gmail.com",
            password=bcrypt.generate_password_hash("ABCDabcd1").decode('utf8'),
            is_admin=True
        ),

        User(
            name="Marco",
            email="marco@gmail.com",
            password=bcrypt.generate_password_hash("ABCDabcd1").decode('utf8')
        ),

        User(
             name="Sam",
             email="sam@gmail.com",
             password=bcrypt.generate_password_hash("ABCDabcd1").decode('utf8')
        )
    ]
    
    accounts = [
        Account(
            account_name = "savings",
            currency_code = "AUD",
            balance = 2000,
            user = users[0]
        ),
        Account(
            account_name = "travel",
            currency_code = "EUR",
            balance = 3500,
            user = users[0]
        ),
        Account(
            account_name = "travel",
            currency_code = "CZK",
            balance = 500,
            user = users[0]
        ),
        Account(
            account_name = "car",
            currency_code = "USD",
            balance = 597,
            user = users[1]
        ),
        Account(
            account_name = "travel",
            currency_code = "JMD",
            balance = 2000,
            user = users[1]
        ),
        Account(
            account_name = "europe-trip",
            currency_code = "EUR",
            balance = 1000,
            user = users[3]
        ),
        Account(
            account_name = "savings",
            currency_code = "CAD",
            balance = 3500,
            user = users[2]
        ),
        Account(
            account_name = "savings",
            currency_code = "USD",
            balance = 300,
            user = users[3]
        ),
        Account(
            account_name = "savings",
            currency_code = "AUD",
            balance = 2811,
            user = users[3]
        )
    ]

    deposits = [
        Deposit(
            amount = 200,
            account = accounts[1]
        ),
        Deposit(
            amount = 1050,
            description = "car",
            account = accounts[2]
        ),
        Deposit(
            amount = 3400,
            description = "Savings",
            account = accounts[0]
        ),
        Deposit(
            amount = 300,
            description = "savings",
            account = accounts[5]
        ),
        Deposit(
            amount = 180,
            account = accounts[3]
        ),
        Deposit(
            amount = 100,
            description = "paycheck",
            account = accounts[3]
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
