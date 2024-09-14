from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    amount_exchanged = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=func.now())

    # foreign keys
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))

    # relationships
    account_origin = db.relationship("Account", foreign_keys=[from_account_id], back_populates="exchange_from")
    account_destination = db.relationship("Account", foreign_keys=[to_account_id], back_populates="exchange_to")


class ExchangeSchema(ma.Schema):
    account_origin = fields.Nested("AccountSchema", only=["account_id", "balance", "currency"])
    account_destination = fields.Nested("AccountSchema", only=["account_id", "balance", "currency"])
    class Meta:
        fields = ("exchange_id", "amount", "account_origin", "account_destination", "amount_exchanged", "description", "date_time")
        ordered = True

exchange_schema = ExchangeSchema()
exchanges_schema = ExchangeSchema(many=True)