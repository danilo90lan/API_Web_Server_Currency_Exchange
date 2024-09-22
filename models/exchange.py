from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Range
from sqlalchemy import func

class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)       # VALIDATED
    amount_exchanged = db.Column(db.Numeric(precision=10, scale=2), nullable=False)     # VALIDATED
    description = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=func.now())

    # foreign keys
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))

    # relationships
    account_origin = db.relationship("Account", foreign_keys=[from_account_id], back_populates="exchange_from")
    account_destination = db.relationship("Account", foreign_keys=[to_account_id], back_populates="exchange_to")


class ExchangeSchema(ma.Schema):
    account_origin = fields.Nested("AccountSchema", only=["account_id", "currency", "user"])
    account_destination = fields.Nested("AccountSchema", only=["account_id", "currency", "user"])

    amount = fields.Float(required=True, validate=Range(min=1, error="Amount must be greater than 0."))

    description = fields.String(validate=Regexp("^[A-Za-z0-9 ]{4,100}$", 
                                                               error="Description must be between 4 and 100 characters, and contain only alphanumeric characters and spaces."))

    class Meta:
        fields = ("exchange_id", "amount", "account_origin", "account_destination", "amount_exchanged", "description", "date_time")
        ordered = True

exchange_schema = ExchangeSchema()
exchanges_schema = ExchangeSchema(many=True)