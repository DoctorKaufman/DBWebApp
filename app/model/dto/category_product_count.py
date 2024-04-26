class CategoryProductCountDTO:
    def __init__(self, category_number, category_name, promotional_products_count, non_promotional_products_count):
        self.__category_number = category_number
        self.__category_name = category_name
        self.__promotional_products_count = promotional_products_count
        self.__non_promotional_products_count = non_promotional_products_count

    @property
    def category_number(self):
        return self.__category_number

    @property
    def category_name(self):
        return self.__category_name

    @property
    def promotional_products_count(self):
        return self.__promotional_products_count

    @property
    def non_promotional_products_count(self):
        return self.__non_promotional_products_count

    def serialize(self):
        return {
            'Category_Num': self.__category_number,
            'Name': self.__category_name,
            'Promotional_Products_Count': self.__promotional_products_count,
            'Non_Promotional_Products_Count': self.__non_promotional_products_count
        }
