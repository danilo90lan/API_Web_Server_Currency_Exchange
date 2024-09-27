from init import db, ma  # db: SQLAlchemy instance, ma: Marshmallow instance for schema validation
from marshmallow import fields  # For defining schema fields in Marshmallow schemas
from marshmallow.validate import Length, And, Regexp, Email  # For field validation (regular expressions, ranges, EMAIL)

class User(db.Model):
    __tablename__ = "users"

    # Defining columns for the 'users' table
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key for each user
    name = db.Column(db.String(20), nullable=False)  # User's name, validated, NOT NULL
    email = db.Column(db.String, nullable=False, unique=True)  # User's email, must be unique and validated
    password = db.Column(db.String, nullable=False)  # Password, validated
    is_admin = db.Column(db.Boolean, default=False)  # A boolean flag to indicate if the user is an admin

    # Relationship with the Account model (user can have multiple accounts)
    # Cascade delete ensures that deleting a user deletes their associated accounts if account.balance=0
    accounts = db.relationship("Account", back_populates="user", cascade="all, delete")

class UserSchema(ma.Schema):
    # Nested field to include the accounts associated with the user in the serialized data
    # It's List because it's one-to-many relationship. (user can have multiple accounts)
    accounts = fields.List(fields.Nested("AccountSchema", only=["account_id", "account_name", "currency"]))

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
            Length(min=8, max=20, error="Password must be between 8 and 20 characters."),
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

    class Meta:
        fields = ("user_id", "name", "email", "password", "is_admin", "accounts")


# This schema instance includes the password field, used for validation purposes (during registration or login)
user_schema_validation = UserSchema()

# Schemas for retrieving user data without exposing the password field
user_schema = UserSchema(exclude=["password"])  # For a single user
users_schema = UserSchema(many=True, exclude=["password"])  # For multiple users