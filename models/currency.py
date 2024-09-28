# db: SQLAlchemy instance for database interaction, ma: Marshmallow instance for schema definition
from init import db, ma
from sqlalchemy import func  # Importing SQL functions like 'now' for timestamps


class Currency(db.Model):
    __tablename__ = "currencies"  # Defining the name of the table in the database

    # Defining the columns for the 'currencies' table
    # Currency code (e.g., USD, EUR) as the primary key (unique)
    currency_code = db.Column(db.String(3), primary_key=True)
    # Exchange rate for the currency, cannot be null
    rate = db.Column(db.Float, nullable=False)
    # Base currency code for the exchange rate (USD)
    base_code = db.Column(db.String(3), nullable=False)
    # Timestamp for when the exchange rate was last updated, defaults to the current time
    last_update = db.Column(db.DateTime, default=func.now())

    # Defining relationships
    # One-to-Many relationship with Account (one currency to many accounts)
    account = db.relationship('Account', back_populates='currency')

# Marshmallow schema


class CurrencySchema(ma.Schema):
    class Meta():
        # Fields that will be included when serializing data
        fields = ("currency_code", "rate", "base_code", "last_update")
        ordered = True  # Ensures the fields are serialized in the order defined here


currency_schema = CurrencySchema()  # For a single currency
# For multiple currencies (a list of currency records)
currencies_schema = CurrencySchema(many=True)
