from flask import Flask, redirect, render_template, request, abort, jsonify
from flask import make_response, url_for

from utils import save_picture_product, save_picture_account

from data import db_session, products_api
from data.products import Products
from data.users import User

from forms.create_products_form import CreateProductsForm
from forms.register_form import RegisterForm
from forms.authorization_form import AuthorizationForm as AutoForm
from forms.edit_account_form import EditAccountForm

# from waitress import serve для vscale

from flask_login import LoginManager, login_user, login_required, current_user, logout_user

# оплата
from cloudipsp import Api, Checkout

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/buy/<int:id>')
def buy(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    if type(product.price) == int:
        data = {
            "currency": "RUB",
            "amount": int(product.price * 100)
        }
    else:
        data = {
            "currency": "RUB",
            "amount": int(''.join((product.price + '00').split(' ')))
        }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


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
    user = db_sess.query(User)
    if current_user.is_authenticated:
        return render_template('index.html', title='Главная', products=products)
    else:
        return render_template('index.html', title='Главная', products=products)


@app.route('/account')
def account():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    date = str(user.register_date).split()[0]
    image_file = url_for('static',
                         filename='img/profile_pics/' + current_user.name + '/account_image/' + current_user.photo)
    return render_template('account.html', title='Аккаунт', user=user, date=date, image_file=image_file)


@app.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    form = EditAccountForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(current_user.id == User.id).first()
        if user:
            form.name_f.data = user.name
            form.surname_f.data = user.surname
            form.age_f.data = user.age
            form.town_f.data = user.town
            form.email_f.data = user.email
            form.password_f.data = user.password
            form.photo_f.data = user.photo
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(current_user.id == User.id).first()
        if user:
            user.name = form.name_f.data
            user.surname = form.surname_f.data
            user.age = form.age_f.data
            user.town = form.town_f.data
            user.email = form.email_f.data
            user.password = form.password_f.data
            if form.photo_f.data:
                photo_file = save_picture_account(form.photo_f.data)
                user.photo = photo_file
            db_sess.commit()
            return redirect('/account')
        else:
            abort(404)
    image_file = url_for('static',
                         filename='img/profile_pics/' + current_user.name + '/account_image/' + current_user.photo)
    return render_template('edit_account.html', title='Редактирование аккаунта', form=form, image_file=image_file)


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
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Products()
        product.product = form.product_f.data
        product.price = form.price_f.data
        product.about = form.about_f.data
        product.user_id = current_user.id
        if form.photo_f.data:
            photo_file = save_picture_product(form.photo_f.data)
            product.photo = photo_file
        db_sess.add(product)
        db_sess.commit()
        return redirect('/')
    # аватарка пользователя
    image_file = url_for('static',
                         filename='img/profile_pics/' + current_user.name + '/account_image/' + current_user.photo)
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
    form = CreateProductsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        product = db_sess.query(Products).filter(Products.id == id).first()
        if product:
            form.product_f.data = product.product
            form.price_f.data = product.price
            form.about_f.data = product.about
            form.photo_f.data = product.photo
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
            return redirect('/account')
        else:
            abort(404)
    return render_template('sell_product.html', title='Редактирование объявления', form=form)


def main():
    db_session.global_init('buynet.sqlite')
    app.register_blueprint(products_api.blueprint)
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()