from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, Email

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)     # VALIDATED
    email = db.Column(db.String, nullable=False, unique=True)      # VALIDATED
    password = db.Column(db.String, nullable=False)     # VALIDATED
    is_admin = db.Column(db.Boolean, default=False)

    accounts = db.relationship("Account", back_populates="user", cascade="all, delete")

class UserSchema(ma.Schema):
    accounts = fields.List(fields.Nested("AccountSchema", only=["account_id", "account_name", "currency"]))

    # Validation
    name = fields.String(required=True, validate=Regexp("^[A-Za-z]{3,20}$", 
                                                    error="User name must be between 3 and 20 characters in length and contain only alphabetic characters with no space."))

    password = fields.String(required=True, validate=And(Length(min=8, max=20, error="Password must be between 8 and 20 characters."),
                                                    Regexp("^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]+$",
                                                    error="Password must contain at least one uppercase letter, one lowercase letter, and one digit, without special characters.")))

    email = fields.String(required=True, validate=Email(error="Invalid email address format."))


    class Meta:
        fields = ("user_id", "name", "email", "password", "is_admin", "accounts")

# This schema contains the password value and it's used for the validation only
user_schema_validation = UserSchema()

# These two schemas are used only for retrieving purposes
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])