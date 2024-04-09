from collections import OrderedDict

from app.model.dto.product import ProductDTO
from app.services.enum.column_type import ColumnType


class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository
        self.column_mapping = {
            'id_product': 'ID',
            'category_number': 'Category ID',
            'product_name': 'Name',
            'p_characteristics': 'Description'
        }

    def get_product_by_id_product(self, id_product):
        return self.product_repository.select_product(id_product)

    def get_all_products(self, pageable):
        return self.product_repository.select_all_products(pageable)

    def create_product(self, product_creation_dto):
        return self.product_repository.insert_product(product_creation_dto)

    def update_product(self, product_dto, id_product):
        product = ProductDTO(id_product, product_dto.category_number, product_dto.product_name,
                             product_dto.p_characteristics)
        self.product_repository.update_product(product)
        return product

    def delete_product(self, product_id):
        self.product_repository.delete_product(product_id)

    def get_product_columns(self):
        columns = self.product_repository.get_column_names()
        prettier_column = ColumnType.map_columns(columns, self.column_mapping)
        prettier_column['Category ID'] = ColumnType.FK.serialize()
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))
