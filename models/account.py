from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2))
    date_creation = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="accounts")
    operations = db.relationship("Operation", back_populates="account")

    exchange_from = db.relationship("ExchangeAccount", foreign_keys='ExchangeAccount.from_account_id', back_populates="account_origin")
    exchanges_to = db.relationship("ExchangeAccount", foreign_keys='ExchangeAccount.to_account_id', back_populates="account_destination")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ("account_id", "currency", "balance", "date_creation", "user")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
