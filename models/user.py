# db: SQLAlchemy instance, ma: Marshmallow instance for schema validation
from init import db, ma
# For defining schema fields in Marshmallow schemas
from marshmallow import fields, validates, ValidationError  
# For field validation (regular expressions, ranges, EMAIL)
from marshmallow.validate import Length, And, Regexp, Email


class User(db.Model):
    __tablename__ = "users"

    # Defining columns for the 'users' table
    # Primary key for each user
    user_id = db.Column(db.Integer, primary_key=True)
    # User's name, validated, NOT NULL
    name = db.Column(db.String(20), nullable=False)
    # User's email, must be unique and validated
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)  # Password, validated
    # A boolean flag to indicate if the user is an admin
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship with the Account model (user can have multiple accounts)
    # Cascade delete ensures that deleting a user deletes their associated accounts if account.balance=0
    accounts = db.relationship(
        "Account", back_populates="user", cascade="all, delete")


class UserSchema(ma.Schema):
    # Nested field to include the accounts associated with the user in the serialized data
    # It's List because it's one-to-many relationship. (user can have multiple accounts)
    accounts = fields.List(fields.Nested("AccountSchema", only=[
                           "account_id", "account_name", "currency"]))

    # Validation for fields
    # Name must be between 3 and 20 characters long, and only alphabetic characters are allowed (no spaces).
    name = fields.String(
        required=True,
        validate=Regexp(
            "^[A-Za-z]{3,20}$",
            error="User name must be between 3 and 20 characters in length and contain only alphabetic characters with no space."
        )
    )

    # Password must be between 8 and 20 characters long, with at least one uppercase letter, one lowercase letter, and one digit. Special characters are not allowed.
    password = fields.String(
        required=True,
        validate=And(
            Length(min=8, max=20,
                   error="Password must be between 8 and 20 characters."),
            Regexp(
                "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)[A-Za-z\\d]+$",
                error="Password must contain at least one uppercase letter, one lowercase letter, and one digit, without special characters."
            )
        )
    )

    # Email is validated using Marshmallow's Email validator).
    email = fields.String(
        required=True,
        validate=Email(error="Invalid email address format.")
    )

    # sanitization for the name, password, and email fields 
    # by validating that they contain only ASCII characters.
    # The isascii() method checks whether all characters in the string are ASCII characters

    @validates("name")
    def validate_name(self, value):
        if not value.isascii():
            raise ValidationError("Name must contain only ASCII characters.")
        return value

    @validates("password")
    def validate_password(self, value):
        if not value.isascii():
            raise ValidationError("Password must contain only ASCII characters.")
        return value

    @validates("email")
    def validate_email(self, value):
        if not value.isascii():
            raise ValidationError("Email must contain only ASCII characters.")
        return value

    class Meta:
        fields = ("user_id", "name", "email",
                  "password", "is_admin", "accounts")


# This schema instance includes the password field, used for validation purposes (during registration or login)
user_schema_validation = UserSchema()

# Schemas for retrieving user data without exposing the password field
user_schema = UserSchema(exclude=["password"])  # For a single user
users_schema = UserSchema(
    many=True, exclude=["password"])  # For multiple users
