from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.controllers.dtos.create.employee_account_creation import EmployeeAccountCreation
from app.model.dto.authorised_user import AuthorisedUserDTO
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from app.model.dto.employee import EmployeeDTO
from app.model.dto.employee_account import EmployeeAccountDTO


class AuthService:
    def __init__(self, auth_repository, employee_repository):
        self.auth_repository = auth_repository
        self.employee_repository = employee_repository

    def authenticate(self, login_data):
        employee = self.auth_repository.get_employee_account_by_login(login_data.login)
        if employee is None or not check_password_hash(employee.password_hash, login_data.password):
            return None
        employee = self.employee_repository.select_employee(employee.id_employee)
        # session["user_id"] = employee.id_employee
        # session["user"] = employee.serialize()
        return AuthorisedUserDTO(employee.id_employee, f'{employee.empl_name} {employee.empl_surname}',
                                 employee.empl_role)

    def register_user(self, register_data, login_data):
        employee = self.auth_repository.get_employee_account_by_login(login_data.login)
        if employee is not None:
            return None
        # employee dto
        db_employee = self.employee_repository.insert_employee(register_data)
        account = EmployeeAccountCreation(login_data.login, generate_password_hash(login_data.password),
                                          db_employee.id_employee)
        self.auth_repository.insert_employee_account(account)
        session["user_id"] = db_employee.id_employee
        return db_employee
