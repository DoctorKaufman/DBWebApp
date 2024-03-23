from flask import Blueprint, request

check = Blueprint('check', __name__, url_prefix='/check')


@check.route('/', methods=['POST'])
def add_check():
    return ''