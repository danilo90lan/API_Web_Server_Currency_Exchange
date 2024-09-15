from init import db
from models.user import User
from flask_jwt_extended import get_jwt_identity

def authorize_as_admin():
    user_id = get_jwt_identity()
    statement = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(statement)
    if user.is_admin == True:
        return True
    else:
        return False
