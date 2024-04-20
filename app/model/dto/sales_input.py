class SalesInputDTO:
    """
    DTO class for input data related to sales calculations.
    """

    def __init__(self, cashier_id=None, start_date=None, end_date=None):
        self.__cashier_id = cashier_id
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def cashier_id(self):
        return self.__cashier_id

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date
