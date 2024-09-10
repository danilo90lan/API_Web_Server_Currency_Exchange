from init import db, ma
from marshmallow import fields
from sqlalchemy import func

class ExchangeAccount(db.Model):
    __tablename__ = "exchanges_accounts"
    exchange_account_id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=func.now())

    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    exchange_id = db.Column(db.Integer, db.ForeignKey("exchanges.exchange_id"), nullable=False)

    from_account = db.relationship("Account", foreign_keys=[from_account_id], back_populates="exchange_from")
    to_account = db.relationship("Account", foreign_keys=[to_account_id], back_populates="exchanges_to")
    exchange = db.relationship("Exchange", back_populates="exchange_account")

class ExchangeAccountSchema(ma.Schema):
    from_account = fields.Nested("AccountSchema", only=["account_id", "currency", "balance"])
    to_account = fields.Nested("AccountSchema", only=["account_id", "currency", "balance"])
    exchange = fields.Nested("ExchangeSchema", exclude=["exchange_account"])
    class Meta:
        fields = ("exchange_account_id",  "exchange", "date_time", "from_account", "to_account")
        ordered = True

exchange_account_schema = ExchangeAccountSchema()
exchanges_accounts_schema = ExchangeAccountSchema(many=True)