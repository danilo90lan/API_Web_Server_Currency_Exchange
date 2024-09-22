import os
from flask import Flask
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import Forbidden

from init import db, ma, bcrypt, jwt
from controllers.cli_controllers import db_commands
from controllers.account_controller import account_bp
from controllers.currency_controller import currency_bp
from controllers.auth_controller import auth_bp

from utils.currency import update_exchange_rates
from apscheduler.schedulers.background import BackgroundScheduler


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialize extensions with the app instance
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Error handling for validation errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    # Error handling for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(err):
        return {"error": f"Resource not found. {err}"}, 404
    
    # Error handling for Forbidden errors
    @app.errorhandler(Forbidden)
    def forbidden_error(error):
        return {"error": error.description}, 403
    
    # General error handling for unexpected exceptions
    @app.errorhandler(Exception)
    def handle_general_error(error):
        return {"error": f"An unexpected error occurred {error}"}, 500
    
    
    # register blueprints
    app.register_blueprint(db_commands)     # CLI commands
    app.register_blueprint(account_bp)      # Account routes
    app.register_blueprint(currency_bp)     # Currency routes
    app.register_blueprint(auth_bp)         # Authentication routes

   
    # Start the background scheduler for updating exchange rates
    scheduler = BackgroundScheduler()
    # Execute update_exchange_rates() every 60 minutes
    scheduler.add_job(func=update_exchange_rates, trigger="interval", minutes=60, args=[app])
    scheduler.start()

    return app