from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2))
    amount_exchanged = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=func.now())

    # foreign keys
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    currency_from = db.Column(db.String(3), db.ForeignKey('currencies.currency_code'), nullable=False)
    currency_to = db.Column(db.String(3), db.ForeignKey('currencies.currency_code'), nullable=False)

    # relationships
    currency_origin = db.relationship("Currency", foreign_keys=[currency_from], back_populates="exchanges_from")
    currency_destination = db.relationship("Currency", foreign_keys=[currency_to], back_populates="exchanges_to")
    account_origin = db.relationship("Account", foreign_keys=[from_account_id], back_populates="exchange_from")
    account_destination = db.relationship("Account", foreign_keys=[to_account_id], back_populates="exchange_to")


class ExchangeSchema(ma.Schema):
    account_origin = fields.Nested("AccountSchema", only=["account_id", "balance"])
    account_destination = fields.Nested("AccountSchema", only=["account_id", "balance"])
    currency_origin = fields.Nested("CurrencySchema", only=["currency_code", "rate", "base_code"])
    currency_destination  = fields.Nested("CurrencySchema", only=["currency_code", "rate", "base_code"])
    class Meta:
        fields = ("exchange_id", "amount", "currency_origin", "amount_exchanged", "currency_destination", "account_origin", "account_destination", "description", "date_time")
        ordered = True

exchange_schema = ExchangeSchema()
exchanges_schema = ExchangeSchema(many=True)