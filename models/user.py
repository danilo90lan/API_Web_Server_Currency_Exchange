from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, Email
from marshmallow.exceptions import ValidationError

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)     # VALIDATED
    email = db.Column(db.String, nullable=False, unique=True)      # VALIDATED
    password = db.Column(db.String, nullable=False)     # VALIDATED
    is_admin = db.Column(db.Boolean, default=False)

    accounts = db.relationship("Account", back_populates="user")

class UserSchema(ma.Schema):
    accounts = fields.List(fields.Nested("AccountSchema", only=["account_id", "account_name", "currency_code"]))

    # Validation
    name = fields.String(required=True, validate=Regexp("^[A-Z][a-z]{2,19}$", 
                                                    error="User name must be between 3 and 20 characters in length, be capitalized and contain only alphabetic characters with no space."))

    password = fields.String(required=True, validate=And(Length(min=8, max=20, error="Password must be between 8 and 20 characters."),
                                                    Regexp("^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]+$",
                                                    error="Password must contain at least one uppercase letter, one lowercase letter, and one digit, without special characters.")))

    email = fields.String(required=True, validate=Email(error="Invalid email address format."))

    # @validates("email")
    # def validates_user_email(self, email):
    #     # check if the email already exist into the database
    #     statement = db.select(User).filter_by(email=email)
    #     existing_email = db.session.scalar(statement)
        
    #     if existing_email:
    #         raise ValidationError("Email is already registered, enter a different email")  # HTTP 409 Conflict


    class Meta:
        fields = ("user_id", "name", "email", "password", "is_admin", "accounts")

user_schema_validation = UserSchema()
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])