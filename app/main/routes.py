from app import db

from app.models import User
from app.models import Permission

from app.decorators import admin_required
from app.decorators import permission_required

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


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@login_required
@permission_required(Permission.WRITE)
def index():
    return render_template('index.html', title='Главная')


@bp.route('/user/<string:username>', methods=['GET'])
@login_required
@permission_required(Permission.WRITE)
def user(username):
    return ''

