class CategoryInputDTO:
    def __init__(self, category_name):
        self.__category_name = category_name

    @property
    def category_name(self):
        return self.__category_name

    @staticmethod
    def deserialize(data):
        category_name = data.get('category_name')
        return CategoryInputDTO(category_name)
