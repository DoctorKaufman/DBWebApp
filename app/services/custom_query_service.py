<<<<<<< HEAD
from app.model.repository.category_in_stock import CategoryInStockRepository
from app.model.repository.customer import CustomerRepository


class CustomQueryService:
    def __init__(self, customer_repository: CustomerRepository, category_stock_repository: CategoryInStockRepository):
        self.customer_repository = customer_repository
        self.category_stock_repository = category_stock_repository

    def get_customers_statistics(self, min_amount: float):
        return self.customer_repository.get_customers(min_amount)

    def get_categories_in_stock(self):
        return self.category_stock_repository.get_categories()
=======
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
>>>>>>> af7b1e6a4225cfc88dc8096acfcfd767d0624f02
