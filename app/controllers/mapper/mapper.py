from app.services.enum.column_type import ColumnType


class CategoryMapper:
    column_mapping = {
        'category_number': 'ID',
        'category_name': 'Name'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, CategoryMapper.column_mapping)
        return prettier_column

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in CategoryMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'category_number')

    @staticmethod
    def map_to_front_column(column):
        return CategoryMapper.column_mapping[column]


class ProductMapper:
    column_mapping = {
        'id_product': 'ID',
        'category_number': 'Category_ID',
        'category_name': 'Category',
        'product_name': 'Name',
        'p_characteristics': 'Description'
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, ProductMapper.column_mapping)
        prettier_column['Category_ID'] = ColumnType.HIDDEN.serialize()
        prettier_column['Category'] = ColumnType.FK.serialize()
        return prettier_column

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in ProductMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'id_product')

    @staticmethod
    def map_to_front_column(column):
        return ProductMapper.column_mapping[column]


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
        return prettier_column

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in CustomerCardMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'card_number')

    @staticmethod
    def map_to_front_column(column):
        return CustomerCardMapper.column_mapping[column]


class StoreProductMapper:
    column_mapping = {
        'upc': 'UPC',
        'upc_prom': 'UPC_Prom',
        'id_product': 'Product_ID',
        'selling_price': 'Price',
        'products_number': 'Amount',
        'promotional_product': 'Promotional_Product',
        'product_name': 'Product_Name',
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, StoreProductMapper.column_mapping)
        prettier_column['UPC_Prom'] = ColumnType.FK.serialize()
        prettier_column['Product_ID'] = ColumnType.HIDDEN.serialize()
        prettier_column['Product_Name'] = ColumnType.FK.serialize()
        return prettier_column

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in StoreProductMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'upc')

    @staticmethod
    def map_to_front_column(column):
        return StoreProductMapper.column_mapping[column]


class EmployeeMapper:
    column_mapping = {
        'id_employee': 'ID',
        'empl_name': 'Name',
        'empl_surname': 'Surname',
        'empl_patronymic': 'Patronymic',
        'empl_role': 'Role',
        'salary': 'Salary',
        'date_of_birth': 'Birth_Date',
        'date_of_start': 'Start_Date',
        'phone_number': 'Phone_Number',
        'city': 'City',
        'street': 'Street',
        'zip_code': 'Zip',
        'login': 'Login',
        'password': 'Password',
    }

    @staticmethod
    def map_columns(columns):
        prettier_column = ColumnType.map_columns(columns, EmployeeMapper.column_mapping)
        prettier_column['Login'] = ColumnType.HIDDEN.serialize()
        prettier_column['Password'] = ColumnType.HIDDEN.serialize()
        return prettier_column

    @staticmethod
    def map_to_db_column(column):
        keys = [key for key, val in EmployeeMapper.column_mapping.items() if val == column]
        return next(iter(keys), 'id_employee')

    @staticmethod
    def map_to_front_column(column):
        return EmployeeMapper.column_mapping[column]
