from app.model.repository.category import CategoryRepository
from app.model.repository.categoty_product_count import CategoryProductCountRepository
from app.model.repository.customer_product import CustomerCardProductRepository


class CustomQueryService:
    def __init__(self, category_product_repository: CategoryProductCountRepository,
                 customer_repository: CustomerCardProductRepository,
                 category_repository: CategoryRepository):
        self.category_product_repository = category_product_repository
        self.customer_repository = customer_repository
        self.category_repository = category_repository

    # def get_customer_card_products(self, category_number: int):
    def get_customer_card_products(self, category_name: str):
        category = self.category_repository.select_category_by_name(category_name)
        return self.customer_repository.get_customer_card_products(category.category_number)

    def get_category_product_counts(self):
        return self.category_product_repository.get_category_product_counts()
