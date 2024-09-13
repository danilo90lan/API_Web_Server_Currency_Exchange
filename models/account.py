from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(precision=10, scale=2))
    date_creation = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    currency_code = db.Column(db.String(3),db.ForeignKey("currencies.currency_code"), nullable=False)
    
    user = db.relationship("User", back_populates="accounts")
    deposits = db.relationship("Deposit", back_populates="account")
    currency = db.relationship('Currency', back_populates='account')
    exchange_from = db.relationship("Exchange", foreign_keys='Exchange.from_account_id', back_populates="account_origin")
    exchange_to = db.relationship("Exchange", foreign_keys='Exchange.to_account_id', back_populates="account_destination")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    exchange_from = fields.List(fields.Nested("ExchangeSchema"), exclude=["account_destination"])
    exchange_to = fields.List(fields.Nested("ExchangeSchema"), exclude=["account_origin"])
    class Meta:
        fields = ("account_id", "currency_code", "balance", "date_creation", "user", "exchange_from", "exchange_to")
        ordered=True

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
