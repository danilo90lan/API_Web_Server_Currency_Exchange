from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency_from = db.Column(db.String(3), nullable=False)
    amount_exchanged = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency_to = db.Column(db.String(3), nullable=False)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=func.now())
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)

    # relationship
    account_origin = db.relationship("Account", foreign_keys=[from_account_id], back_populates="exchange_from")
    account_destination = db.relationship("Account", foreign_keys=[to_account_id], back_populates="exchange_to")


class ExchangeSchema(ma.Schema):
    account_origin = fields.Nested("AccountSchema", only=["account_id", "currency", "balance"])
    account_destination = fields.Nested("AccountSchema", only=["account_id", "currency", "balance"])
    class Meta:
        fields = ("exchange_id", "amount", "currency_from", "amount_exchanged", "currency_to", "description", "account_origin", "account_destination", "date_time")
        ordered = True

exchange_schema = ExchangeSchema()
exchanges_schema = ExchangeSchema(many=True)