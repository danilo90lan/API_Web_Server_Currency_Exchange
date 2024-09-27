from init import db, ma  # db is the SQLAlchemy database instance, ma is the Marshmallow instance for serialization and validation
from marshmallow import fields, validates  # Fields for Marshmallow schemas and validation methods
from marshmallow.validate import OneOf, And, Regexp, Range  # Validators for Marshmallow
from marshmallow.exceptions import ValidationError  # Handling validation exceptions

from sqlalchemy import func  # Used to get SQL functions like the current timestamp (now())
from flask_jwt_extended import get_jwt_identity  # For JWT token identity retrieval

from models.user import User  # Importing the User model for relationships
from utils.currency import get_currencies_codes  # A utility function to retrieve valid currency codes

# Fetching valid currency codes for validation purpose 
# (get_currencies_code retrieve all the currency_codes from the third-party API response and return it into a tuple.)
VALID_CURRENCY_CODES = get_currencies_codes()

class Account(db.Model):
    __tablename__ = "accounts"
    # Defining the columns of the accounts table
    account_id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each account
    account_name = db.Column(db.String(20), nullable=False)  # Account name, must be validated
    balance = db.Column(db.Numeric(precision=10, scale=2), default=0)  # Account balance, numeric with 2 decimal places, default value is 0
    date_creation = db.Column(db.DateTime, default=func.now())  # Date when the account is created, defaults to current time

     # Foreign key references to other tables
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)  # Foreign key linking to users table
    currency_code = db.Column(db.String(3), db.ForeignKey("currencies.currency_code"), nullable=False)  # Currency code, must be validated
    
   # Defining relationships with other models
    user = db.relationship("User", back_populates="accounts") 
    deposits = db.relationship("Deposit", back_populates="account", cascade="all, delete")  # Relationship with deposits, cascade deletion if account is deleted
    currency = db.relationship("Currency", back_populates='account')  
    
    # Exchange model has multiplerelationship with the same Account table need to specify which foreign key to use for each relationship.
    # the Exchange table has two foreign keys referencing the Account table. One for the "from" account and another for the "to" account.
    exchange_from = db.relationship("Exchange", foreign_keys="Exchange.from_account_id", back_populates="account_origin")  
    exchange_to = db.relationship("Exchange", foreign_keys="Exchange.to_account_id", back_populates="account_destination")  

class AccountSchema(ma.Schema):
    # Nested relationships, only selecting specific fields to serialize
    user = fields.Nested("UserSchema", only=["user_id", "name"])    # Serialize only user_id and name from the related User model
    currency = fields.Nested("CurrencySchema", only=["currency_code", "rate"])  # Serialize only currency_code and rate from the related Currency model

    # Validation
    # Alphanumeric characters, between 3 and 20 characters
    account_name = fields.String(required=True, validate=Regexp("^[A-Za-z0-9]{3,20}$",  
                                                                error="Title must be between 3 and 20 characters in length and contain alphanumeric characters only!"))
    
    # Ensures the currency code is exactly 3 uppercase letters
    # Ensures that the currency code is one of the valid currency codes from the utility function
    currency_code = fields.String(required=True, validate=And(Regexp("^[A-Z]{3}$", error="Currency code must be Upper-case and exactly 3 characters in length."),
                                               OneOf(VALID_CURRENCY_CODES)))        
    
    # Ensures that the balance is float type and non-negative
    balance = fields.Float(validate=Range(min=0, error="Balance cannot be negative."))

    @validates("currency_code")
    def validates_currency_code(self, currency_code):
        """
        Validate the currency code to ensure that the user
        does not have another account with the same currency code.
        """

        # Retrieve the user_id from the JWT
        user_id = get_jwt_identity()
        # Check if there's an existing account with the same currency_code for this user

        # SELECT Account.*
        # FROM Account
        # JOIN User ON Account.user_id = User.user_id
        # WHERE Account.currency_code = (currency_code) AND Account.user_id = (user_id)
        # LIMIT 1;

        existing_account = (
        db.session.query(Account)
        .join(User, Account.user_id == User.user_id)
        .filter(Account.currency_code == currency_code, Account.user_id == user_id)
        .first()     # Get the first matching account, if any
    ) 
        # Raise a validation error if an existing account is found
        if existing_account:
            raise ValidationError(f"An account with the currency {currency_code} already exists for the user {user_id}")

    class Meta:
        # Fields that will be included when serializing data
        fields = ("account_id", "account_name", "balance", "currency_code", "date_creation", "currency", "user")
        ordered=True

account_schema = AccountSchema()        # For a single currency
accounts_schema = AccountSchema(many=True)      # For multiple currencies (a list of currency records)