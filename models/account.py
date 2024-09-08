from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2))
    date_creation = db.Column(db.DateTime, default=func.now())
    last_update = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    user = user = db.relationship("User", back_populates="accounts")

class AccountSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ("account_id", "balance", "date_creation", "last_update", "user")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
