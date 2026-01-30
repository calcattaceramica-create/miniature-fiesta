from flask import Blueprint

bp = Blueprint('hr', __name__)

from app.hr import routes

