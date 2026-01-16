from flask import Blueprint

bp = Blueprint('purchases', __name__)

from app.purchases import routes

