class StoreProductService:

    def __init__(self, store_product_repository):
        self.store_product_repository = store_product_repository

    def get_store_product_by_upc(self, upc):
        return self.store_product_repository.select_store_product(upc)

    def get_all_store_products(self, pageable):
        return self.store_product_repository.select_all_store_products(pageable)

    def create_store_product(self, store_product_dto):
        return self.store_product_repository.insert_store_product(store_product_dto)

    def delete_store_product(self, upc):
        return self.store_product_repository.delete_store_product(upc)

    def get_store_product_columns(self):
        return self.store_product_repository.get_column_names()
