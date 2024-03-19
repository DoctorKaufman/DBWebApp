from flask import Blueprint, request
product = Blueprint('product', __name__, url_prefix='/product')


@product.route('/', methods=['POST'])
def create_product():
    return ''


@product.route('/<int:product_id>/', methods=['PUT'])
def update_product(product_id):
    return ''


@product.route('/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    return ''


@product.route('/', methods=['GET'])
def get_all_products():
    return ''


