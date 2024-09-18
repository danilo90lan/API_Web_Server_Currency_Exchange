from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Range
from sqlalchemy import func

class Deposit(db.Model):
    __tablename__ = "deposits"
    deposit_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)   # VALIDATED
    description = db.Column(db.String)      #VALIDATED
    date_time = db.Column(db.DateTime, default=func.now())
    
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"))

    account = db.relationship("Account", back_populates="deposits")

class DepositSchema(ma.Schema):
    account = fields.Nested("AccountSchema", only=["account_id", "currency", "balance", "user"])

    # validation
    amount = fields.Float(validate=Range(min=1, error="Amount must be greater than 0."))

    description = fields.String(required=True, validate=Regexp("^[A-Za-z0-9 ]{10,100}$", 
                                                               error="Description must be between 10 and 100 characters, and contain only alphanumeric characters and spaces."))


    class Meta:
        fields = ("deposit_id", "amount", "description", "date_time", "account")
        ordered=True
        
deposit_schema = DepositSchema()
deposits_schema = DepositSchema(many=True)