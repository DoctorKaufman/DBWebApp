class ProductBuyDTO:
    def __init__(self, upc, amount, price):
        self.__upc = upc
        self.__amount = amount
        self.__price = price

    @property
    def upc(self):
        return self.__upc

    @property
    def amount(self):
        return self.__amount

    def set_amount(self, amount):
        self.__amount = amount

    @property
    def price(self):
        return self.__price

    @staticmethod
    def deserialize(data):
        return ProductBuyDTO(int(data['upc']), int(data['amount']), float(data['price']))