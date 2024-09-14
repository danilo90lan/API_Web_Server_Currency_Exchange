from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Deposit(db.Model):
    __tablename__ = "deposits"
    operation_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=func.now())
    
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)

    account = db.relationship("Account", back_populates="deposits")

class DepositSchema(ma.Schema):
    account = fields.Nested("AccountSchema", only=["account_id", "currency", "balance", "user"])
    class Meta:
        fields = ("operation_id", "amount", "description", "date_time", "account")
        ordered=True
        
deposit_schema = DepositSchema()
deposits_schema = DepositSchema(many=True)