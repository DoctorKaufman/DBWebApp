import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.mapper.mapper import EmployeeMapper
from app.model.repository.employee import EmployeeRepository
from app.services.employee_service import EmployeeService

employee = Blueprint('employee', __name__, url_prefix='/employee')

employee_repository = EmployeeRepository(get_connection())
employee_service = EmployeeService(employee_repository)


@employee.route('/', methods=['GET'])
def get_all_employees():
    args = request.args
    employees = employee_service.get_all_employees(Pageable.get_pageable(args, EmployeeMapper))
    return json.dumps([e.serialize() for e in employees]), 200

@employee.route('/columns', methods=['GET'])
def get_columns():
    # return json.dumps(employee_service.get_employee_columns())
    return employee_service.get_employee_columns()


# @employee.route('/', methods=['POST'])
# def add_employee():
#     return ''
#
#
# @employee.route('/<int:id>/', methods=["PUT"])
# def update_employee(id):
#     return ''
#
#
# @employee.route('/<int:id>/', methods=['DELETE'])
# def delete_employee(id):
#     return ''
#
#
# @employee.route('/<int:id>/', methods=['GET'])
# def get_employee(id):
#     return ''
#
#
# @employee.route('/', methods=['GET']) #TODO pagination using url param employee?sorting=desc&page=5&size=10 etc.
# def get_all_employee():
#     data = request.args
#     print(data)
#     return ''


@employee.route('/by-role/<employee_role>/', methods=['GET'])
def get_employee_by_role(employee_role):
    return ''
