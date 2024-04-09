class ProductCreationDTO:
    def __init__(self, category_number, product_name, p_characteristics):
        self.__category_number = category_number
        self.__product_name = product_name
        self.__p_characteristics = p_characteristics

    @property
    def category_number(self):
        return self.__category_number

    @property
    def product_name(self):
        return self.__product_name

    @property
    def p_characteristics(self):
        return self.__p_characteristics

    @staticmethod
    def deserialize(data):
        category_number = data.get('category_number')
        product_name = data.get('product_name')
        p_characteristics = data.get('p_characteristics')
        return ProductCreationDTO(category_number, product_name, p_characteristics)