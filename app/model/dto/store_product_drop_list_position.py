class StoreProductDropListPositionDTO:
    def __init__(self, upc, product_name):
        self.__upc = upc
        self.__product_name = product_name

    @property
    def category_number(self):
        return self.__upc

    @property
    def product_name(self):
        return self.__product_name

    def serialize(self):
        return {
            self.__upc: self.__product_name
        }
