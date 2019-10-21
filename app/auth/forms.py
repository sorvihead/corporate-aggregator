from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    password = PasswordField('Password', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                       Length(min=4,
                                              max=20,
                                              message="Логин должен быть длиною от 4 до 20 символов"),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Имя пользователя может включать в себя'
                                                                             'только латинские буквы, цифры,'
                                                                             'точку и нижнее подчеркивание')])
    email = StringField('Email',
                        validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                    Email(message="Неверный Email")])
    password = PasswordField('Password',
                             validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                         Length(min=8,
                                                max=30,
                                                message="Пароль должен быть длиною от 8 до 30 символов")])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                          EqualTo('password',
                                                  message="Пароли не совпадают")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь с таким логином уже существует, попробуйте использовать другой логин')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким почтовым адресом уже зарегистрирован')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                    Email(message="Неверный Email")])
    submit = SubmitField('Отправить письмо с подтверждением')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                         Length(min=8,
                                                max=30,
                                                message="Пароль должен быть длиною от 8 до 30 символов")])
    password2 = PasswordField('Password',
                              validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                          EqualTo('password',
                                                  message="Пароли не совпадают")])
    submit = SubmitField('Сбросить пароль')
