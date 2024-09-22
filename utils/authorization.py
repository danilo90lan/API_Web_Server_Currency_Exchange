from init import db
from models.user import User
from models.account import Account
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


def authorize_as_admin():
    """
    Checks if the current user is an admin based on their JWT identity.
    Returns True if the user is an admin, False otherwise.
    """
    try:
        user_id = get_jwt_identity()

        # SELECT *
        # FROM User
        # WHERE user_id = :user_id
        statement = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(statement)
        
        if user.is_admin == True:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        return {"error": f"Database operation failed: {str(e)}"}, 500


def check_account_user(func):
    @wraps(func)
    def wrapper(account_id, *args, **kwargs):
        """
        Decorator to ensure the current user owns the account.
        It checks if the `account_id` provided in the route belongs to the authenticated user.
        """

        # Get the user_id from the JWT
        user_id = int(get_jwt_identity())

        # Check if the origin account belongs to the current user
        # SELECT *
        # FROM Account
        # WHERE account_id = (account_id)
        origin_account = db.session.scalar(db.select(Account).filter_by(account_id=account_id))
        
        # Check if the account exists
        if not origin_account:
            return {"error": f"The account ID {account_id} does NOT exist!"}, 404
        
        # Verify the account belongs to the authenticated user
        if origin_account.user_id != user_id:
            return {"error": f"The account ID {account_id} does NOT belong to the current user!"}, 403
        
        # Proceed to the original function if all checks pass
        return func(account_id, *args, **kwargs)
    return wrapper