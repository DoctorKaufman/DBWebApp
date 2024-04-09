class StoreProductDTO:
    def __init__(self, upc, upc_prom, id_product, selling_price, products_number, promotional_product):
        self.__upc = upc
        self.__upc_prom = upc_prom
        self.__id_product = id_product
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
            'Price': str(self.__selling_price),
            'Amount': self.__products_number,
            'UPC_PROM': self.__upc_prom,
            'ID Product': self.__id_product,
            'Promotional product': self.__promotional_product
            # 'upc': self.__upc,
            # 'upc_prom': self.__upc_prom,
            # 'id_product': self.__id_product,
            # 'selling_price': self.__selling_price,
            # 'products_number': self.__products_number,
            # 'promotional_product': self.__promotional_product
        }
