import json

import flask
from flask import Blueprint, request, session, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    unset_jwt_cookies

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.create.employee_creation import EmployeeCreationDTO
from app.controllers.dtos.login import LoginDTO
from app.model.repository.employee import EmployeeRepository
from app.model.repository.employee_account import EmployeeAccountRepository
from app.services.auth_service import AuthService

auth = Blueprint('auth', __name__, url_prefix='/auth')

auth_repository = EmployeeAccountRepository(get_connection())
employee_repository = EmployeeRepository(get_connection())
auth_service = AuthService(auth_repository, employee_repository)


@auth.route('/login', methods=['POST'])
def login():
    login_data = LoginDTO.deserialize(request.get_json())
    authenticated = auth_service.authenticate(login_data)
    if authenticated is not None:
        access_token = create_access_token(identity=authenticated.id)
        refresh_token = create_refresh_token(identity=authenticated.id)

        response = make_response(authenticated.serialize())
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        # response.set_cookie('user', str(authenticated.serialize()))
        response.set_cookie('id', 'abc')
        response.set_cookie('user123', authenticated.username)
        response.set_cookie('role', authenticated.position)
        return response, 200
    return "", 401


@auth.route('/register', methods=['POST'])
def register():
    employee_data = EmployeeCreationDTO.deserialize(request.get_json())
    login_data = LoginDTO.deserialize(request.get_json())
    authenticated = auth_service.register_user(employee_data, login_data)
    return authenticated.serialize(), 201


@auth.route('/logout')
def logout():
    session.clear()
    response = jsonify()
    unset_jwt_cookies(response)
    return ""


@auth.route('/update_password', methods=['PUT'])
# @login_required
def update_password():
    login_data = LoginDTO.deserialize(request.get_json())
    auth_service.update_password(login_data)
    return "", 200
