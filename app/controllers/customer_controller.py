from flask import Blueprint, request

customer = Blueprint('customer', __name__, url_prefix='/customer')


@customer.route('/', methods=['POST'])
def create_customer():
    return ''


@customer.route('/<int:id>/', methods=['PUT'])
def update_customer(id):
    return ''


@customer.route('/<int:id>/', methods=['DELETE'])
def delete_customer(id):
    return ''


@customer.route('/<int:id>/', methods=['GET'])
def get_customer(id):
    return ''


@customer.route('/', methods=['GET']) #TODO Pagination
def get_all_customers():
    return ''


