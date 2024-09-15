from models.account import Account
from init import db

from flask_jwt_extended import get_jwt_identity

def check_account_user(account_id):
    # check if the account exists
    statement = db.select(Account).filter_by(account_id=account_id)
    account = db.session.scalar(statement)
    if not account:
        return {"error":"The account does NOT exist!"}, 404

    # Get the user_id from JWT identity
    user_id = int(get_jwt_identity())
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return {"error": f"The account {account_id} doesn NOT belong to the current user"}
    else:
        return True
