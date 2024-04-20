from app.controllers.handler.exceptions import ValidationException


class CategoryCreationDTO:
    def __init__(self, category_name):
        self.__category_name = category_name

    @property
    def category_name(self):
        return self.__category_name

    @staticmethod
    def deserialize(data):
        category_name = data.get('Name')
        if category_name is None or len(category_name) == 0:
            raise ValidationException("Category name cannot be empty")
        return CategoryCreationDTO(category_name)
