from init import db
from models.currency import Currency

def convert_currency(amount, origin, destination):
    """
Convert an amount from Currency A to Currency B using USD as the base.

"""
    
    statement = db.select(Currency).filter_by(currency_code=origin)
    from_code = db.session.scalar(statement)
    statement = db.select(Currency).filter_by(currency_code=destination)
    to_code = db.session.scalar(statement)

    conversion = (amount / from_code.rate) * to_code.rate
    return conversion

