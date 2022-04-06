from flask import Flask, redirect, render_template, request, abort, jsonify
from flask import make_response, url_for

from utils import save_picture_product

from data import db_session
from data.products import Products
from data.users import User

from forms.create_products_form import CreateProductsForm
from forms.register_form import RegisterForm
from forms.authorization_form import AuthorizationForm as AutoForm

from flask_login import LoginManager, login_user, login_required, current_user, logout_user


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


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = AutoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email_f.data).first()
        pas = db_sess.query(User).filter(User.password == form.password_f.data).first()

        if user and pas:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        else:
            return render_template('authorization.html', message='Неправильный логин или пароль',
                                   form=form, title='Войти')
    return render_template('authorization.html', title='Войти', form=form)


@app.route('/')
@app.route('/index')
def home():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).all()
    return render_template('index.html', title='Главная', products=products)


@app.route('/account')
def account():
    return render_template('account.html', title='Акаунт')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email_f.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже зарегистрирован')
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/sell_product', methods=['GET', 'POST'])
@login_required
def sell_product():
    form = CreateProductsForm()
    print('Инициализировали окно')
    if form.validate_on_submit():
        print('Нажали на кнопку')
        db_sess = db_session.create_session()
        product = Products()
        product.product = form.product_f.data
        product.price = form.price_f.data
        product.photo = form.photo_f.data
        product.about = form.about_f.data
        product.user_id = current_user.id
        print('Дошли до функции сохранения')
        print(form.photo_f.data)
        photo_file = save_picture_product(form.photo_f.data)
        print('Сохранили')
        product.photo = photo_file
        db_sess.add(product)
        db_sess.commit()
        return redirect('/')
    # аватарка пользователя
    print('аватарка пользователя')
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.name + '/products_image' +
                         current_user.photo)
    print('возврат')
    return render_template('sell_product.html', title='Объявление',
                           form=form, image_file=image_file)


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def poduct_delete(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Products).filter(Products.id == id).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    print(5)
    form = CreateProductsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        product = db_sess.query(Products).filter(Products.id == id).first()
        print(product.product)
        if product:
            print('Yes')
            form.product_f.data = product.product
            form.price_f.data = product.price
            form.about_f.data = product.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = db_sess.query(Products).filter(Products.id == id).first()
        if product:
            product.product = form.product_f.data
            product.photo = form.photo_f.data
            product.price = form.price_f.data
            product.about = form.about_f.data
            photo_file = save_picture_product(form.photo_f.data)
            product.photo = photo_file
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('sell_product.html', title='Редактирование объявления', form=form)


def main():
    db_session.global_init('buynet.sqlite')
    app.run()


if __name__ == '__main__':
    main()