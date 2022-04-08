import secrets
import os
from flask_login import current_user
from flask import current_app
from PIL import Image


# создаём уникальное имя изображения и сохраняем его
def save_picture_product(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'img', 'profile_pics', current_user.name, 'products_image')
    if not os.path.isdir(full_path):
        os.makedirs(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (330, 700)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_picture_account(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'img', 'profile_pics', current_user.name, 'account_image')
    if not os.path.isdir(full_path):
        os.makedirs(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (300, 300)
    print(form_picture)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn