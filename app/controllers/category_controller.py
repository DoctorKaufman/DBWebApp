from flask import Blueprint, request

category = Blueprint('category', __name__, url_prefix='/category')


@category.route('/', methods=['POST'])
def create_category():
    return ''


@category.route('/<int:category_id>/', methods=['PUT'])
def update_category(category_id):
    return ''


@category.route('/<int:category_id>/', methods=['DELETE'])
def delete_category(category_id):
    return ''


@category.route('/<int:category_id>/', methods=['GET'])
def get_category(category_id):
    return ''


@category.route('/', methods=['GET'])
def get_all_categories():
    return ''




