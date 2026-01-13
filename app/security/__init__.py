from flask import Blueprint

bp = Blueprint('security', __name__, url_prefix='/security')

from app.security import routes

