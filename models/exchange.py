from init import db, ma
from marshmallow import fields

class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency_from = db.Column(db.String(3), nullable=False)
    amount_exchanged = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency_to = db.Column(db.String(3), nullable=False)
    description = db.Column(db.String)

    exchange_account = db.relationship("ExchangeAccount", back_populates="exchange")


class ExchangeSchema(ma.Schema):
    exchange_account = fields.List(fields.Nested("ExchangeAccountSchema"), exclude="exchange")
    class Meta:
        fields = ("exchange_id", "amount", "currency_from", "amount_exchanged", "currency_to", "description", "exchange_account")
        ordered = True

exchange_schema = ExchangeSchema()
exchanges_shema = ExchangeSchema(many=True)