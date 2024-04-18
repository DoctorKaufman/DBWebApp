from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.model.dto.authorised_user import AuthorisedUserDTO


class AuthService:
    def __init__(self, auth_repository, employee_repository):
        self.auth_repository = auth_repository
        self.employee_repository = employee_repository

    def authenticate(self, login_data):
        print(generate_password_hash(login_data.password))
        employee = self.auth_repository.get_employee_account_by_login(login_data.login)
        if employee is None or not check_password_hash(employee.password_hash, login_data.password):
            return None
        session["user_id"] = employee.id_employee
        employee = self.employee_repository.select_employee(employee.id_employee)
        return AuthorisedUserDTO(employee.id_employee, f'{employee.empl_name} {employee.empl_surname}',
                                 employee.empl_role)

    # def register_user(self, login_data):
    #     employee = self.auth_repository.get_employee_account_by_login(login_data.login)
    #     if employee is not None
    #         return None
    #
