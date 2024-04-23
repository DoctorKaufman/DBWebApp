class ProductDTO:
    def __init__(self, id_product, category_number, product_name, p_characteristics):
        self.__id_product = id_product
        self.__category_number = category_number
        self.__product_name = product_name
        self.__p_characteristics = p_characteristics

    @property
    def id_product(self):
        return self.__id_product

    @property
    def category_number(self):
        return self.__category_number

    @property
    def product_name(self):
        return self.__product_name

    @property
    def p_characteristics(self):
        return self.__p_characteristics

    def serialize(self):
        return {
            'ID': self.__id_product,
            'Category_ID': self.__category_number,
            'Name': self.__product_name,
            'Description': self.__p_characteristics
            # 'id_product': self.__id_product,
            # 'category_number': self.__category_number,
            # 'product_name': self.__product_name,
            # 'p_characteristics': self.__p_characteristics
        }
