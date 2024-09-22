from models.currency import Currency, currencies_schema

from init import db
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for currency routes
currency_bp = Blueprint("currencies", __name__, url_prefix="/currencies")

@currency_bp.route("/")
@jwt_required()         # Ensure the user is authenticated
def get_all_currencies():
    """
    retrieve all currency records from the database, 
    ensuring that the data is sorted
    """
    try: 
        # SELECT * 
        # FROM Currency 
        # ORDER BY currency_code;
        statement = db.select(Currency).order_by(Currency.currency_code)
        accounts = db.session.scalars(statement)
        return jsonify(currencies_schema.dump(accounts))
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {e}"}, 500 