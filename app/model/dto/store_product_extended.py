class StoreProductExtendedDTO:
    def __init__(self, upc, upc_prom, id_product, product_name, selling_price, products_number, promotional_product):
        self.__upc = upc
        self.__upc_prom = upc_prom
        self.__id_product = id_product
        self.__product_name = product_name
        self.__selling_price = selling_price
        self.__products_number = products_number
        self.__promotional_product = promotional_product

    @property
    def upc(self):
        return self.__upc

    @property
    def upc_prom(self):
        return self.__upc_prom

    @property
    def id_product(self):
        return self.__id_product

    @property
    def product_name(self):
        return self.__product_name

    @property
    def selling_price(self):
        return self.__selling_price

    @property
    def products_number(self):
        return self.__products_number

    @property
    def promotional_product(self):
        return self.__promotional_product

    def serialize(self):
        return {
            'UPC': self.__upc,
            'UPC Prom': self.__upc_prom,
            'Product ID': self.__id_product,
            'Price': str(self.__selling_price),
            'Amount': self.__products_number,
            'Promotional Product': self.__promotional_product,
            'Product Name': self.__product_name
        }
