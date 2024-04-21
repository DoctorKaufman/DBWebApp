import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.dtos.create.employee_creation import EmployeeCreationDTO
from app.controllers.dtos.login import LoginDTO
from app.controllers.mapper.mapper import EmployeeMapper
from app.model.repository.employee import EmployeeRepository
from app.model.repository.employee_account import EmployeeAccountRepository
from app.services.auth_service import AuthService
from app.services.employee_service import EmployeeService

employee = Blueprint('employee', __name__, url_prefix='/employee')

auth_repository = EmployeeAccountRepository(get_connection())
employee_repository = EmployeeRepository(get_connection())
employee_service = EmployeeService(employee_repository)
auth_service = AuthService(auth_repository, employee_repository)


@employee.route('/', methods=['GET'])
def get_all_employees():
    args = request.args
    employees = employee_service.get_all_employees(Pageable.get_pageable(args, EmployeeMapper))
    return json.dumps([e.serialize() for e in employees]), 200


@employee.route('/columns', methods=['GET'])
def get_columns():
    # return json.dumps(employee_service.get_employee_columns())
    return json.dumps(employee_service.get_employee_columns())


@employee.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(EmployeeMapper.map_to_front_column(employee_service.get_pk_name())), 200


@employee.route('/register', methods=['POST'])
def register():
    employee_data = EmployeeCreationDTO.deserialize(request.get_json())
    login_data = LoginDTO.deserialize(request.get_json())
    authenticated = auth_service.register_user(employee_data, login_data)
    return authenticated.serialize(), 201


@employee.route('/<int:employee_id>', methods=['PUT'])
def update(employee_id):
    employee_data = EmployeeCreationDTO.deserialize(request.get_json())
    return json.dumps(employee_service.update_employee(employee_data, employee_id).serialize()), 200


@employee.route('/<int:employee_id>', methods=['DELETE'])
def delete(employee_id):
    if employee_service.delete_employee(employee_id):
        return '', 204
    else:
        return '', 404
