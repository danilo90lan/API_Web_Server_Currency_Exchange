from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.account import Account
from datetime import datetime

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped!")

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
            last_update = datetime.now(),
            user = users[0]
        ),
            Account(
            currency = "EUR",
            balance = 3500.76,
            date_creation = datetime.now(),
            last_update = datetime.now(),
            user = users[0]
        ),
            Account(
            currency = "USD",
            balance = 597,
            date_creation = datetime.now(),
            last_update = datetime.now(),
            user = users[1]
        ),
            Account(
            currency = "USD",
            balance = 300,
            date_creation = datetime.now(),
            last_update = datetime.now(),
            user = users[2]
        )
    ]

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
