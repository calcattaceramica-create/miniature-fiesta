from flask import Blueprint

bp = Blueprint('accounting', __name__)

from app.accounting import routes

