from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf
from sqlalchemy import func

from utils.currency import get_currencies_codes

VALID_CURRENCY_CODES = get_currencies_codes()

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String, default="FUNDS") # VALIDATED
    description = db.Column(db.String)
    balance = db.Column(db.Numeric(precision=10, scale=2), default=0)
    date_creation = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    currency_code = db.Column(db.String(3),db.ForeignKey("currencies.currency_code"), nullable=False)
    
    user = db.relationship("User", back_populates="accounts")
    deposits = db.relationship("Deposit", back_populates="account")
    currency = db.relationship("Currency", back_populates='account')
    exchange_from = db.relationship("Exchange", foreign_keys='Exchange.from_account_id', back_populates="account_origin")
    exchange_to = db.relationship("Exchange", foreign_keys='Exchange.to_account_id', back_populates="account_destination")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["user_id", "name"])
    currency = fields.Nested("CurrencySchema", only=["currency_code", "rate"])

    # Validation
    account_name = fields.String(validate=Length(min=4, error="Title must be at least 4 characthers in length."))
    currency_code = fields.String(validate=OneOf(VALID_CURRENCY_CODES))
    
    class Meta:
        fields = ("account_id", "account_name", "balance", "currency_code", "description", "date_creation", "currency", "user")
        ordered=True

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)