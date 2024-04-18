import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.login import LoginDTO
from app.controllers.dtos.registration import RegistrationDTO
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
        return authenticated.serialize(), 200
    return "", 401


@auth.route('/register', methods=['POST'])
def register():
    registration_data = RegistrationDTO.deserialize(request.get_json())
    authenticated = auth_service.authenticate(registration_data)

