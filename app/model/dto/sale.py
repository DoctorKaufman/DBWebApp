class SaleDTO:
    def __init(self, upc, check_number, product_number, selling_price):
        self.__upc = upc
        self.__check_number = check_number
        self.__product_number = product_number
        self.__selling_price = selling_price

    @property
    def upc(self):
        return self.__upc

    @property
    def check_number(self):
        return self.__check_number

    @property
    def product_number(self):
        return self.__product_number

    @property
    def selling_price(self):
        return self.__selling_price
