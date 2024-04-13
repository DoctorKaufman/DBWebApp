from app.controllers.handler.exceptions import DataDuplicateException
from app.controllers.mapper.mapper import ProductMapper
from app.model.dto.product import ProductDTO


class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def get_product_by_id_product(self, id_product):
        # return self.product_repository.select_product(id_product)
        return self.product_repository.select_product(id_product)

    def get_all_products(self, pageable):
        # return self.product_repository.select_all_products(pageable)
        return self.product_repository.select_all_products_extended(pageable)

    def create_product(self, product_creation_dto):
        if self.product_name_exists(product_creation_dto.product_name):
            raise DataDuplicateException("Product with such name already exists")
        return self.product_repository.insert_product(product_creation_dto)

    def update_product(self, product_dto, id_product):
        product_name = product_dto.product_name
        if (self.product_name_exists(product_name) and product_name != self.product_repository
                .select_product(id_product).product_name):
            raise DataDuplicateException("Product with such name already exists")

        product = ProductDTO(id_product, product_dto.category_number, product_dto.product_name,
                             product_dto.p_characteristics)
        self.product_repository.update_product(product)
        return product

    def delete_product(self, product_id):
        self.product_repository.delete_product(product_id)

    def get_product_columns(self):
        # return ProductMapper.map_columns(self.product_repository.get_column_names())
        return ProductMapper.map_columns(self.product_repository.get_column_names_extended())

    def get_drop_list(self):
        return self.product_repository.select_products_drop_list()

    def get_pk_name(self):
        return self.product_repository.get_primary_key_name()

    def product_name_exists(self, product_name):
        return self.product_repository.exists_product(product_name)
