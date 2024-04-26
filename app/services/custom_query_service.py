from app.model.repository.category_total_cost import CategoryTotalCostRepository
from app.model.repository.employee_all_customers import EmployeeAllCustomersRepository


class CustomQueryService:
    def __init__(self, category_repository: CategoryTotalCostRepository,
                 employee_repository: EmployeeAllCustomersRepository):
        self.category_repository = category_repository
        self.employee_repository = employee_repository

    def get_category_total_cost(self, given_number: float):
        return self.category_repository.get_category_total_cost(given_number)

    def get_employees(self):
        return self.employee_repository.get_employees()
