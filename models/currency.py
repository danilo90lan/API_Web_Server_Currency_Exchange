from init import db, ma

class Currency(db.Model):
    __tablename__ = "currencies"
    currency_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    base_code = db.Column(db.String(3), nullable=False)
    last_update = db.Column(db.Date)

class CurrencySchema(ma.Schema):
    class Meta():
        fields = ("currency_id", "currency", "rate", "base_code", "last_update")