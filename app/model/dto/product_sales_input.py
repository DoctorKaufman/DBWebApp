class ProductSalesInputDTO:
    def __init__(self, product_id, start_date, end_date):
        self.__product_id = product_id
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def product_id(self):
        return self.__product_id

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date
