from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize SQLAlchemy for database ORM (Object-Relational Mapping)
db = SQLAlchemy()

# Initialize Marshmallow for object serialization/deserialization and validation
ma = Marshmallow()

# Initialize Bcrypt for hashing and verifying passwords
bcrypt = Bcrypt()

# Initialize JWTManager for handling JSON Web Token (JWT) authentication
jwt = JWTManager()
