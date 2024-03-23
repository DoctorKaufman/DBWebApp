from flask import Blueprint, request

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/', methods=['POST'])
def add_employee():
    return ''


@employee.route('/<int:id>/', methods=["PUT"])
def update_employee(id):
    return ''


@employee.route('/<int:id>/', methods=['DELETE'])
def delete_employee(id):
    return ''


@employee.route('/<int:id>/', methods=['GET'])
def get_employee(id):
    return ''


@employee.route('/', methods=['GET']) #TODO pagination using url param employee?sorting=desc&page=5&size=10 etc.
def get_all_employee():
    data = request.args
    print(data)
    return ''


@employee.route('/by-role/<employee_role>/', methods=['GET'])
def get_employee_by_role(employee_role):
    return ''