from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed


class CreateProductsForm(FlaskForm):
    product_f = StringField('Название товара',
                            validators=[DataRequired()])
    price_f = StringField('Цена',
                          validators=[DataRequired()])
    photo_f = FileField('Изображение (png, jpg)', default='default.jpg', validators=[FileAllowed(['png', 'jpg'])])
    about_f = StringField('Описание')
    submit = SubmitField('Опубликовать')