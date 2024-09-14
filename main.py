import os
from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt
from controllers.cli_controllers import db_commands
from controllers.exchange_controllers import exchange_bp
from controllers.account_controller import account_bp
from controllers.currency_controller import currency_bp
from controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(account_bp)
    app.register_blueprint(currency_bp)
    app.register_blueprint(auth_bp)
   
    return app