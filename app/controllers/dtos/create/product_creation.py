from app.controllers.handler.exceptions import ValidationException


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
        category_number = data.get('Category_ID')
        product_name = data.get('Name')
        p_characteristics = data.get('Description')
        if category_number is None:
            raise ValidationException('Category ID is missing')
        if product_name is None or len(product_name) == 0:
            raise ValidationException('Name cannot be empty')
        if p_characteristics is None or len(p_characteristics) == 0:
            raise ValidationException('Description of product cannot be empty')
        return ProductCreationDTO(category_number, product_name, p_characteristics)