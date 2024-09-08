from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2))
    date_creation = db.Column(db.DateTime, default=func.now())
    last_update = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="accounts")
    operations = db.relationship("Operation", back_populates="account")

    sender_exchange = db.relationship("Exchange", back_populates="sender_account")
    # exchanges_to = db.relationship("Exchange", back_populates="destination_account")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    operations = fields.List(fields.Nested("OperationSchema"), exclude="account")
    sender_exchange = fields.List(fields.Nested("ExchangeSchema"), exclude=["sender_account", "destination_account"])
    
    class Meta:
        fields = ("account_id", "currency", "balance", "date_creation", "last_update", "user", "operations", "sender_exchange")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
