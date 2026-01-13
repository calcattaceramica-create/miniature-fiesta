from flask import Blueprint

bp = Blueprint('pos', __name__)

from app.pos import routes

