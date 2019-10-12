from app import db

from app.models import User

from app.main import bp

from app.main.forms import *

from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app
from flask import render_template
from flask import g

from flask_login import login_required
from flask_login import current_user

from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Главная')


@bp.route('/user/<string:username>', methods=['GET'])
@login_required
def user(username):
    return ''

