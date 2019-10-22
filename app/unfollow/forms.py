from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Optional
from wtforms.validators import ValidationError

from app.models import Department
from app.models import Shop


class EditForm(FlaskForm):
    name = StringField('Как Вас зовут?', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    surname = StringField('Ваша фамилия', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    about_me = StringField('Расскажите о себе', validators=[Optional()])
    position = StringField('Ваша должность', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    submit = SubmitField("Подтвердить")


class ChoiceForm(FlaskForm):
    shop = StringField("Название магазина, либо его код",
                       validators=[DataRequired(message="Это поле обязательно для заполнения")])
    department = StringField("Название отдела",
                             validators=[DataRequired(message="Это поле обязательно для заполнения")])
    submit = SubmitField("Подтвердить")

    def validate_shop(self, shop_name):
        shop = Shop.query.filter(Shop.name == shop_name.data or Shop.shop_code == shop_name.data).first()
        if not shop:
            raise ValidationError("Такой магазин отсутствует")  # TODO показать ближайшие к введенному значению

    def validate_department(self, department_name):
        department = Department.query.filter_by(name=department_name.data).first()
        if not department:
            raise ValidationError("Такой отдел отсутствует")


class CreateShopForm(FlaskForm):
    name = StringField("Название магазина",
                       validators=[DataRequired(message="Это поле обязательно для заполнения")])
    shop_code = StringField("Код магазина",
                            validators=[DataRequired(message="Это поле обязательно для заполнения")])
    submit = SubmitField("Создать")