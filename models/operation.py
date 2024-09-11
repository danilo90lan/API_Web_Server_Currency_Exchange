from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Operation(db.Model):
    __tablename__ = "operations"
    operation_id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=func.now())

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)

    account = db.relationship("Account", back_populates="operations")

class OperationSchema(ma.Schema):
    account = fields.Nested("AccountSchema", only=["account_id", "currency", "balance"])
    class Meta:
        fields = ("operation_id", "operation_type", "currency", "amount", "description", "date_time", "account")
        ordered=True
        
operation_schema = OperationSchema()
operations_schema = OperationSchema(many=True)