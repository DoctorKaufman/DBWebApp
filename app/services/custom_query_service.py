from app.model.repository.categoty_product_count import CategoryProductCountRepository
from app.model.repository.customer_product import CustomerCardProductRepository


class CustomQueryService:
    def __init__(self, category_repository: CategoryProductCountRepository,
                 customer_repository: CustomerCardProductRepository):
        self.category_repository = category_repository
        self.customer_repository = customer_repository

    def get_customer_card_products(self, category_number: int):
        return self.customer_repository.get_customer_card_products(category_number)

    def get_category_product_counts(self):
        return self.category_repository.get_category_product_counts()
