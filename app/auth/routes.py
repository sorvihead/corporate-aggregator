from app import db

from app.models import User

from app.auth import bp

from app.auth.forms import LoginForm
from app.auth.forms import RegistrationForm
from app.auth.forms import ResetPasswordForm
from app.auth.forms import ResetPasswordRequestForm

#from app.auth.email import send_password_reset_email

from flask import flash
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # main.index

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверный логин или пароль")
            redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.login')  # main.index
        return redirect(next_page)
    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    return 200
