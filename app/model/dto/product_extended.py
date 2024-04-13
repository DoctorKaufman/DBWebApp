class ProductExtendedDTO:
    def __init__(self, id_product, category_number, category_name, product_name, p_characteristics):
        self.__id_product = id_product
        self.__category_number = category_number
        self.__category_name = category_name
        self.__product_name = product_name
        self.__p_characteristics = p_characteristics

    @property
    def id_product(self):
        return self.__id_product

    @property
    def category_number(self):
        return self.__category_number

    @property
    def category_name(self):
        return self.__category_name

    @property
    def product_name(self):
        return self.__product_name

    @property
    def p_characteristics(self):
        return self.__p_characteristics

    def serialize(self):
        return {
            'ID': self.__id_product,
            'Name': self.__product_name,
            'Category': self.__category_name,
            'Category ID': self.__category_number,
            'Description': self.__p_characteristics
        }
