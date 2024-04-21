from app.controllers.mapper.mapper import EmployeeMapper
from app.model.dto.employee import EmployeeDTO


class EmployeeService:
    def __init__(self, employee_repository):
        self.employee_repository = employee_repository

    def get_all_employees(self, pageable):
        return self.employee_repository.select_all_employees(pageable)

    def get_employee_columns(self):
        return EmployeeMapper.map_columns(self.employee_repository.get_column_names())

    def get_pk_name(self):
        return self.employee_repository.get_primary_key_name()

    def update_employee(self, employee_data, employee_id):
        employee = EmployeeDTO(employee_id, employee_data.empl_surname, employee_data.empl_name,
                               employee_data.empl_patronymic, employee_data.empl_role, employee_data.salary,
                               employee_data.date_of_birth, employee_data.date_of_start, employee_data.phone_number,
                               employee_data.city, employee_data.street, employee_data.zip_code)
        self.employee_repository.update_employee(employee)
        return employee

    def delete_employee(self, employee_id):
        return self.employee_repository.delete_employee(employee_id)
