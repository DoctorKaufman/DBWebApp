from collections import OrderedDict

from app.services.enum.column_type import ColumnType


class CategoryMapper:
    column_mapping = {
        'category_number': 'ID',
        'category_name': 'Name'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, CategoryMapper.column_mapping)
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))

    @staticmethod
    def map_column(column):
        return CategoryMapper.column_mapping[column]

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in CategoryMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'category_number')


class ProductMapper:
    column_mapping = {
        'id_product': 'ID',
        'category_number': 'Category ID',
        'product_name': 'Name',
        'p_characteristics': 'Description'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, ProductMapper.column_mapping)
        prettier_column['Category ID'] = ColumnType.FK.serialize()
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in ProductMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'id_product')


class CustomerCardMapper:
    column_mapping = {
        'card_number': 'ID',
        'cust_surname': 'Surname',
        'cust_name': 'Name',
        'cust_patronymic': 'Patronymic',
        'phone_number': 'PhoneNum',
        'city': 'City',
        'street': 'Street',
        'zip_code': 'Zip',
        'c_percent': 'Percent'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, CustomerCardMapper.column_mapping)
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in CustomerCardMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'card_number')


class StoreProductMapper:
    column_mapping = {
        'upc': 'UPC',
        'upc_prom': 'UPC Prom',
        'id_product': 'Product ID',
        'selling_price': 'Price',
        'products_number': 'Amount',
        'promotional_product': 'Promotional Product'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, StoreProductMapper.column_mapping)
        prettier_column['UPC Prom'] = ColumnType.FK.serialize()
        prettier_column['Product ID'] = ColumnType.FK.serialize()
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in StoreProductMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'upc')
