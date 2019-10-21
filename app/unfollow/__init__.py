from flask import Blueprint

bp = Blueprint('unfollow', __name__)

from app.unfollow import routes