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

# Define a Blueprint for database management commands
db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    """
    This command creates all tables in the database based on the current models.
    It also seeds the currency table with initial data.
    """

    # Create all tables as defined by SQLAlchemy models
    db.create_all()
    print("Tables created")
    # Initialize currency table by seeding data from an external API
    seed_currency_table()


@db_commands.cli.command("drop")
def drop_tables():
    """
    This command drops all tables from the database.
    Useful for resetting the database during development.
    """

    # Connect to the application context to interact with the database
    with current_app.app_context():
        # Reflect the current database structure
        db.reflect()
        # This will drop all tables
        db.drop_all()
        print("All tables dropped successfully")


@db_commands.cli.command("seed")
def seed_database():
    """
    This command seeds the database with initial data for users, accounts, and deposits.
    """

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
            account_name="savings",
            currency_code="AUD",
            balance=2000,
            user=users[0]     # Account is linked to user Danilo
        ),
        Account(
            account_name="travel",
            currency_code="EUR",
            balance=3500,
            user=users[0]
        ),
        Account(
            account_name="travel",
            currency_code="CZK",
            balance=500,
            user=users[0]
        ),
        Account(
            account_name="car",
            currency_code="USD",
            balance=597,
            user=users[1]     # Account is linked to user Alberto
        ),
        Account(
            account_name="travel",
            currency_code="JMD",
            balance=2000,
            user=users[1]
        ),
        Account(
            account_name="europe-trip",
            currency_code="EUR",
            balance=1000,
            user=users[3]     # Account is linked to user Sam
        ),
        Account(
            account_name="savings",
            currency_code="CAD",
            balance=3500,
            user=users[2]     # Account is linked to user Marco
        ),
        Account(
            account_name="savings",
            currency_code="USD",
            balance=300,
            user=users[3]
        ),
        Account(
            account_name="savings",
            currency_code="AUD",
            balance=2811,
            user=users[3]
        )
    ]

    deposits = [
        Deposit(
            amount=200,
            # Deposit linked to account with currency_code EUR
            account=accounts[1]
        ),
        Deposit(
            amount=1050,
            description="car",
            # Deposit linked to account with currency_code CZK
            account=accounts[2]
        ),
        Deposit(
            amount=3400,
            description="Savings",
            # Deposit linked to account with currency_code AUD
            account=accounts[0]
        ),
        Deposit(
            amount=300,
            description="savings",
            # Deposit linked to account with currency_code EUR
            account=accounts[5]
        ),
        Deposit(
            amount=180,
            # Deposit linked to account with currency_code USD
            account=accounts[3]
        ),
        Deposit(
            amount=100,
            description="paycheck",
            account=accounts[3]       # Another deposit for the USD account
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
        # In case of any errors, roll back the transaction to prevent partial commits
        db.session.rollback()
        return {"error": f"Database operation failed {e}"}, 500
