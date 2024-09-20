from init import db
from models.user import User
from models.account import Account
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


def authorize_as_admin():
    try:
        user_id = get_jwt_identity()
        statement = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(statement)
        if user.is_admin == True:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {str(e)}"}, 500


# check if the account ID belongs to the current user
def check_account_user(account_id):
    try:
        # check if the account exists
        statement = db.select(Account).filter_by(account_id=account_id)
        account = db.session.scalar(statement)
        if not account:
            return {"error":f"The account ID {account_id} does NOT exist!"}, 404

        # Get the user_id from JWT identity
        user_id = int(get_jwt_identity())
        # Check if the account belongs to the user

        if account.user_id == user_id:
            return True 
        else:
            return {"error": f"The account ID {account_id} doesn NOT belong to the current user!"}
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {str(e)}"}, 500


def check_account_user(func):
    @wraps(func)
    def wrapper(account_id, destination_id=None, *args, **kwargs):
        # Get the user_id from the JWT
        user_id = int(get_jwt_identity())
        
        # Check if the origin account belongs to the current user
        origin_account = db.session.scalar(db.select(Account).filter_by(account_id=account_id))
        if not origin_account:
            return {"error": f"The account ID {account_id} does NOT exist!"}, 404
        if origin_account.user_id != user_id:
            return {"error": f"The account ID {account_id} does NOT belong to the current user!"}, 403
        
        # If a destination account ID is provided, check if it also belongs to the current user
        if destination_id:
            destination_account = db.session.scalar(db.select(Account).filter_by(account_id=destination_id))
            if not destination_account:
                return {"error": f"The account ID {destination_id} does NOT exist!"}, 404
            if destination_account.user_id != user_id:
                return {"error": f"The account ID {destination_id} does NOT belong to the current user!"}, 403
        
            return func(account_id, destination_id, *args, **kwargs)
        
        return func(account_id, *args, **kwargs)
    
    return wrapper