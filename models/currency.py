from init import db, ma  # db: SQLAlchemy instance for database interaction, ma: Marshmallow instance for schema definition
from sqlalchemy import func  # Importing SQL functions like 'now' for timestamps

class Currency(db.Model):
    __tablename__ = "currencies"  # Defining the name of the table in the database
    
    # Defining the columns for the 'currencies' table
    currency_code = db.Column(db.String(3), primary_key=True)  # Currency code (e.g., USD, EUR) as the primary key (unique)
    rate = db.Column(db.Float, nullable=False)  # Exchange rate for the currency, cannot be null
    base_code = db.Column(db.String(3), nullable=False)  # Base currency code for the exchange rate (USD)
    last_update = db.Column(db.DateTime, default=func.now())  # Timestamp for when the exchange rate was last updated, defaults to the current time

    # Defining relationships
    account = db.relationship('Account', back_populates='currency')  # One-to-Many relationship with Account (one currency to many accounts)

# Marshmallow schema
class CurrencySchema(ma.Schema):
    class Meta():
        # Fields that will be included when serializing data
        fields = ("currency_code", "rate", "base_code", "last_update") 
        ordered = True  # Ensures the fields are serialized in the order defined here

currency_schema = CurrencySchema()  # For a single currency
currencies_schema = CurrencySchema(many=True)  # For multiple currencies (a list of currency records)