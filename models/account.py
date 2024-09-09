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

    exchange_from = db.relationship("Exchange", foreign_keys='Exchange.from_account_id', back_populates="from_account")
    exchanges_to = db.relationship("Exchange", foreign_keys='Exchange.to_account_id', back_populates="to_account")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    operations = fields.List(fields.Nested("OperationSchema"), exclude="account")
    exchange_from = fields.List(fields.Nested("ExchangeSchema"))
    exchange_to = fields.List(fields.Nested("ExchangeSchema"))
    
    class Meta:
        fields = ("account_id", "currency", "balance", "date_creation", "user", "operations")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
