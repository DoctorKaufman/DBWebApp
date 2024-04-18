from app.controllers.mapper.mapper import EmployeeMapper


class EmployeeService:
    def __init__(self, employee_repository):
        self.employee_repository = employee_repository

    def get_all_employees(self, pageable):
        return self.employee_repository.select_all_employees(pageable)

    def get_employee_columns(self):
        return EmployeeMapper.map_columns(self.employee_repository.get_column_names())
