from models.account import Account, accounts_schema, account_schema

from init import db
from flask import Blueprint, request, jsonify
from datetime import datetime


account_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

@account_bp.route("/")
def get_all_accounts():
    statement = db.select(Account)
    accounts = db.session.scalars(statement)

    return jsonify(accounts_schema.dump(accounts))