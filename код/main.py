from flask import Flask, redirect, render_template, request, abort, jsonify
from flask import make_response
from data import db_session
from data.products import Products
from data.users import User
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, login_required, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


########################################################


@app.route('/authorization')
def authorization():
    return render_template('authorization.html', title='Войти')


@app.route('/')
@app.route('/index')
def home():
    print('home')
    db_sess = db_session.create_session()
    products = db_sess.query(Products).all()
    return render_template('index.html', title='Главная', products=products)


@app.route('/account')
def account():
    return render_template('account.html', title='Акаунт')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(0)
    if form.validate_on_submit():
        print('click')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email_f.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже зарегистрирован')
        print(1)
        user = User()
        user.name = form.name_f.data
        user.surname = form.surname_f.data
        user.age = form.age_f.data
        user.town = form.town_f.data
        user.email = form.email_f.data
        user.password = form.password_f.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/sell_product')
def sell_product():
    return render_template('sell_product.html', title='Объявление')


def main():
    db_session.global_init('buynet.sqlite')
    app.run()


if __name__ == '__main__':
    main()