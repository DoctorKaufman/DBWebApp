from app.controllers.handler.exceptions import ValidationException


class StoreProductCreationDTO:
    def __init__(self, upc_prom, id_product, selling_price, products_number, promotional_product):
        self.__upc_prom = upc_prom
        self.__id_product = id_product
        self.__selling_price = selling_price
        self.__products_number = products_number
        self.__promotional_product = promotional_product

    @property
    def upc_prom(self):
        return self.__upc_prom

    @property
    def id_product(self):
        return self.__id_product

    @property
    def selling_price(self):
        return self.__selling_price

    @property
    def products_number(self):
        return self.__products_number

    @property
    def promotional_product(self):
        return self.__promotional_product

    @staticmethod
    def deserialize(data):
        upc_prom = data.get("UPC_Prom")
        id_product = data.get("Product_ID")
        selling_price = float(data.get("Price"))
        products_number = float(data.get("Amount"))
        promotional_product = parse_bool(data.get("Promotional_Product"))
        if id_product is None:
            raise ValidationException("ID is not provided")
        if selling_price <= 0:
            raise ValidationException("Selling price must be greater than 0")
        if products_number <= 0:
            raise ValidationException("Product number must be greater than 0")
        return StoreProductCreationDTO(upc_prom, id_product, selling_price, products_number, promotional_product)


def parse_bool(value):
    return str(value).lower() == "true"
