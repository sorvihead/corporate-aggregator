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
from wtforms.validators import Optional


class EditForm(FlaskForm):
    name = StringField('Как Вас зовут?', validators=DataRequired(message="Это поле обязательно для заполнения"))
    surname = StringField('Ваша фамилия', validators=DataRequired(message="Это поле обязательно для заполнения"))
    about_me = StringField('Расскажите о себе', validators=[Optional()])
    position = StringField('Ваша должность', validators=[DataRequired(message="Это поле обязательно для заполнения")])


class ChoiceForm(FlaskForm):
    pass