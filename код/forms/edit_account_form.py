from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from wtforms.fields.html5 import EmailField


class EditAccountForm(FlaskForm):
    photo_f = FileField('Фотография', validators=[FileAllowed(['png', 'jpg'])])
    name_f = StringField('Имя', validators=[DataRequired()])
    surname_f = StringField('Фамилия', validators=[DataRequired()])
    age_f = StringField('Имя', validators=[DataRequired()])
    town_f = StringField('Город', validators=[DataRequired()])
    email_f = EmailField('Почта', validators=[DataRequired()])
    password_f = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')