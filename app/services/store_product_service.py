from app.controllers.mapper.mapper import StoreProductMapper
from app.model.dto.store_product import StoreProductDTO


class StoreProductService:

    def __init__(self, store_product_repository):
        self.store_product_repository = store_product_repository

    def get_store_product_by_upc(self, upc):
        return self.store_product_repository.select_store_product(upc)

    def get_all_store_products(self, pageable):
        # return self.store_product_repository.select_all_store_products(pageable)
        return self.store_product_repository.select_all_store_products_extended(pageable)

    def get_promotional_products(self, is_promotional):
        return self.store_product_repository.select_promotional_products(is_promotional)

    def create_store_product(self, store_product_dto):
        return self.store_product_repository.insert_store_product(store_product_dto)

    def delete_store_product(self, upc):
        return self.store_product_repository.delete_store_product(upc)

    def update_store_product(self, upc, store_product_dto):
        store_product = StoreProductDTO(upc, store_product_dto.upc_prom, store_product_dto.id_product,
                                        store_product_dto.selling_price, store_product_dto.products_number,
                                        store_product_dto.promotional_product)
        self.store_product_repository.update_store_product(store_product)
        return store_product

    def get_store_product_columns(self):
        # return StoreProductMapper.map_columns(self.store_product_repository.get_column_names())
        return StoreProductMapper.map_columns(self.store_product_repository.get_column_names_extended())

    def get_drop_list(self):
        return self.store_product_repository.select_store_products_drop_list()

    def get_pk_name(self):
        return self.store_product_repository.get_primary_key_name()
