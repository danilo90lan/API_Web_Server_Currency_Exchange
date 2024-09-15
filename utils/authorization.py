from init import db
from models.user import User
from models.account import Account
from flask_jwt_extended import get_jwt_identity

def authorize_as_admin():
    user_id = get_jwt_identity()
    statement = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(statement)
    if user.is_admin == True:
        return True
    else:
        return False

# check if the account ID belongs to the current user
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
