class ProductDropListPositionDTO:
    def __init__(self, id_product, product_name):
        self.__id_product = id_product
        self.__product_name = product_name

    @property
    def id_product(self):
        return self.__id_product

    @property
    def product_name(self):
        return self.__product_name

    def serialize(self):
        return {
            self.__id_product: self.__product_name
        }
