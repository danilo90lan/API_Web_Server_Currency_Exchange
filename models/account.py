from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError

from sqlalchemy import func
from flask_jwt_extended import get_jwt_identity
from models.user import User
from utils.currency import get_currencies_codes

VALID_CURRENCY_CODES = get_currencies_codes()

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(20), nullable=False) # VALIDATED
    description = db.Column(db.String(100))  # VALIDATED
    balance = db.Column(db.Numeric(precision=10, scale=2), default=0) # VALIDATED
    date_creation = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    currency_code = db.Column(db.String(3),db.ForeignKey("currencies.currency_code"), nullable=False)  # VALIDATED
    
    user = db.relationship("User", back_populates="accounts")
    deposits = db.relationship("Deposit", back_populates="account")
    currency = db.relationship("Currency", back_populates='account')
    exchange_from = db.relationship("Exchange", foreign_keys='Exchange.from_account_id', back_populates="account_origin")
    exchange_to = db.relationship("Exchange", foreign_keys='Exchange.to_account_id', back_populates="account_destination")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["user_id", "name", "email"])
    currency = fields.Nested("CurrencySchema")

    # Validation
    account_name = fields.String(required=True, validate=Regexp("^[A-Za-z0-9]{4,20}$", 
                                                                error="Title must be between 4 and 20 characters in length and contain alphanumeric characters only!"))
    
    description = fields.String(required=True, validate=Regexp("^[A-Za-z0-9 ]{10,100}$", 
                                                               error="Description must be between 10 and 100 characters, and contain only alphanumeric characters and spaces."))
    
    currency_code = fields.String(validate=And(Regexp("^[A-Z]{3}$", error="Currency code must be Upper-case and exactly 3 characters in length."),
                                               OneOf(VALID_CURRENCY_CODES)))
    
    balance = fields.Float(validate=Range(min=0, error="Balance cannot be negative."))

    @validates("currency_code")
    def validates_status(self, value):
        # retrieve the user_id
        user_id = get_jwt_identity()
        # Check if there's an existing account with the same currency_code for this user
        existing_account = (
        db.session.query(Account)
        .join(User, Account.user_id == User.user_id)
        .filter(Account.currency_code == value, Account.user_id == user_id)
        .first()
    ) 
        # Check if an account with the same currency_code already exists
        if existing_account:
            raise ValidationError(f"An account with this currency code already exists for the user {user_id}")

    class Meta:
        fields = ("account_id", "account_name", "balance", "currency_code", "description", "date_creation", "currency", "user")
        ordered=True

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)