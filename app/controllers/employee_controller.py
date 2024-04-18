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


@employee.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(EmployeeMapper.map_to_front_column(employee_service.get_pk_name())), 200

