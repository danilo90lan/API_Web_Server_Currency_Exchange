# db: SQLAlchemy instance, ma: Marshmallow instance for schema validation
from init import db, ma
from marshmallow import fields  # For defining schema fields
# For field validation (regular expressions, ranges)
from marshmallow.validate import Regexp, Range
from sqlalchemy import func  # For SQL functions such as 'now' to generate timestamps


class Exchange(db.Model):
    __tablename__ = "exchanges"

    # Defining columns for the 'exchanges' table
    # Primary key for each exchange transaction
    exchange_id = db.Column(db.Integer, primary_key=True)
    # Amount exchanged (validated to be non-negative)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    # The amount received after the exchange, validated similarly
    amount_exchanged = db.Column(db.Numeric(
        precision=10, scale=2), nullable=False)
    # Optional description for the exchange
    description = db.Column(db.String(100))
    # Timestamp of when the exchange happened, defaults to the current time
    date_time = db.Column(db.DateTime, default=func.now())

    # Foreign keys to link exchange to 'from' and 'to' accounts
    # Account the amount is being exchanged from, nullable on account deletion (SET NULL) in order to keep the history trace in case the account is deleted
    from_account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.account_id", ondelete='SET NULL'))

    # Account the exchanged amount is being deposited to, nullable on account deletion (SET NULL) in order to keep the history trace in case the account is deleted
    to_account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.account_id", ondelete='SET NULL'))

    # The Exchange model has multiple foreign keys referencing the same related Account model, the foreign_keys parameter
    # helps SQLAlchemy determine which column to use for which relationship.

    # Relationship with the origin account (account sending the amount)
    account_origin = db.relationship("Account", foreign_keys=[
                                     from_account_id], back_populates="exchange_from")

    # Relationship with the destination account (account receiving the exchanged amount)
    account_destination = db.relationship(
        "Account", foreign_keys=[to_account_id], back_populates="exchange_to")


class ExchangeSchema(ma.Schema):
    # Nested fields to include details of the origin and destination accounts
    account_origin = fields.Nested(
        "AccountSchema", only=["account_id", "currency", "user"])

    account_destination = fields.Nested(
        "AccountSchema", only=["account_id", "currency", "user"])

    # Validation
    # Ensures the amount to be exchanged is positive (MIN=1)
    amount = fields.Float(required=True, validate=Range(
        min=1, error="Amount must be greater than 0."))

    # Validates the description to ensure it's between 4 and 100 characters, containing only alphanumeric characters and spaces
    description = fields.String(validate=Regexp("^[A-Za-z0-9 ]{4,100}$",
                                                error="Description must be between 4 and 100 characters, and contain only alphanumeric characters and spaces."))

    class Meta:
        fields = ("exchange_id", "amount", "account_origin",
                  "account_destination", "amount_exchanged", "description", "date_time")
        ordered = True


exchange_schema = ExchangeSchema()  # For serializing a single exchange
# For serializing multiple exchanges (a list of exchanges)
exchanges_schema = ExchangeSchema(many=True)
