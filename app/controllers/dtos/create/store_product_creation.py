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
        upc_prom = data.get("upc_prom")
        id_product = data.get("id_product")
        selling_price = data.get("selling_price")
        products_number = data.get("products_number")
        promotional_product = data.get("promotional_product")
        return StoreProductCreationDTO(upc_prom, id_product, selling_price, products_number, promotional_product)
