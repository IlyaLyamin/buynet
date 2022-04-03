from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name_f = StringField('Имя', validators=[DataRequired()])
    surname_f = StringField('Фамилия', validators=[DataRequired()])
    age_f = StringField('Имя', validators=[DataRequired()])
    town_f = StringField('Город', validators=[DataRequired()])
    email_f = EmailField('Почта', validators=[DataRequired()])
    password_f = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')