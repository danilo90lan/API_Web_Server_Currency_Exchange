# db: SQLAlchemy instance, ma: Marshmallow instance for schema validation
from init import db, ma
from marshmallow import fields  # For defining schema fields
# For field validation (regular expressions, ranges)
from marshmallow.validate import Regexp, Range
# For using SQL functions such as 'now' to generate timestamps
from sqlalchemy import func


class Deposit(db.Model):
    __tablename__ = "deposits"

    # Defining the columns for the 'deposits' table
    deposit_id = db.Column(db.Integer, primary_key=True)  # Primary key
    # Amount deposited (decimal with 2 decimal places), cannot be null
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.String)  # Optional description of the deposit
    # Timestamp of the deposit, defaults to the current time
    date_time = db.Column(db.DateTime, default=func.now())

    # Foreign key linking the deposit to an account
    # Foreign key linking to the 'accounts' table
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"))

    # Relationship with the Account model (one account can have multiple deposits)
    account = db.relationship("Account", back_populates="deposits")

# Marshmallow schema


class DepositSchema(ma.Schema):
    # Nested field to include specific information about the associated account when retrieving
    account = fields.Nested("AccountSchema", only=[
                            "account_id", "balance", "currency"])

    # Validation
    # Ensures that the amount to deposit is float type and non-negative
    amount = fields.Float(required=True, validate=Range(
        min=1, error="Amount must be greater than 0."))

    # Validates the description to ensure it's between 4 and 100 characters and contains only alphanumeric characters and spaces
    description = fields.String(validate=Regexp("^[A-Za-z0-9 ]{4,100}$",
                                                error="Description must be between 4 and 100 characters, and contain only alphanumeric characters and spaces."))

    class Meta:
        fields = ("deposit_id", "amount",
                  "description", "date_time", "account")
        ordered = True  # Ensure the fields are serialized in the specified order


deposit_schema = DepositSchema()  # For serializing a single deposit
# For serializing multiple deposits (a list of deposits)
deposits_schema = DepositSchema(many=True)
