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
