from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    accounts = db.relationship("Account", back_populates="user")

class UserSchema(ma.Schema):
     accounts = fields.List(fields.Nested("AccountSchema", exclude=["user"]))
     class Meta:
        fields = ("user_id", "name", "email", "password", "is_admin", "accounts")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])