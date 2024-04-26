class CategoryTotalCostDTO:
    def __init__(self, category_number, category_name, total_cost, total_quantity):
        self.__category_number = category_number
        self.__category_name = category_name
        self.__total_cost = total_cost
        self.__total_quantity = total_quantity

    @property
    def category_number(self):
        return self.__category_number

    @property
    def category_name(self):
        return self.__category_name

    @property
    def total_cost(self):
        return self.__total_cost

    @property
    def total_quantity(self):
        return self.__total_quantity

    def serialize(self):
        return {
            'Category_Number': self.__category_number,
            'Category_Name': self.__category_name,
            'Total_Cost': float(self.__total_cost),
            'Total_Quantity': int(self.__total_quantity)
        }
