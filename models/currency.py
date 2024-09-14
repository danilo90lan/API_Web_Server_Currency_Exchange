from init import db, ma

class Currency(db.Model):
    __tablename__ = "currencies"
    currency_code = db.Column(db.String(3), primary_key=True)
    rate = db.Column(db.Float, nullable=False)
    base_code = db.Column(db.String(3), nullable=False)
    last_update = db.Column(db.Date)

    account = db.relationship('Account', back_populates='currency')
    deposit = db.relationship('Deposit', back_populates='currency')

class CurrencySchema(ma.Schema):
    class Meta():
        fields = ("currency_code", "rate", "base_code", "last_update")

currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)