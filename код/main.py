from flask import Flask, redirect, render_template, request, abort, jsonify
from flask import make_response
from data import db_session
from data.products import Products
from data.users import User
from flask_login import LoginManager, login_user, login_required, current_user
from base64 import b16decode, b16encode
from io import BytesIO


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/authorization')
def authorization():
    return render_template('authorization.html')


@app.route('/')
@app.route('/index')
def home():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).all()
    return render_template('index.html', title='Главная', products=products)


def main():
    db_session.global_init('buynet.sqlite')
    app.run()


if __name__ == '__main__':
    main()