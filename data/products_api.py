import flask
from flask import jsonify, request
from . import db_session
from .products import Products


blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/products')
def get_products():
    db_sess = db_session.create_session()
    product = db_sess.query(Products).all()
    if product:
        return jsonify(
            {
                'product':
                    [item.to_dict(only=('id', 'author.name', 'product', 'price', 'photo', 'about'))
                     for item in product]
            }
        )


@blueprint.route('/api/products/<int:id>', methods=['GET'])
def get_one_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(id)
    if not product:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {
                'product': product.to_dict(only=(
                    'author.name', 'product', 'price', 'photo', 'about'))
            }
        )


@blueprint.route('/api/products', methods=['POST'])
def create_product():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['user_id', 'product', 'price', 'about']):
        return jsonify({'error': 'bad request'})
    db_sess = db_session.create_session()
    product = Products()
    product.user_id = request.json['user_id']
    product.product = request.json['product']
    product.price = request.json['price']
    product.about = request.json['about']
    db_sess.add(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/products/<int:id>', methods=['DELETE'])
def detete_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(id)
    if not product:
        return jsonify({'error': 'Not found'})
    db_sess.delete(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})

