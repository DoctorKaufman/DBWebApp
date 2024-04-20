class CashierSalesDTO:
    def __init__(self, cashier_id, empl_surname, empl_name, total_sales):
        self.__cashier_id = cashier_id
        self.__empl_surname = empl_surname
        self.__empl_name = empl_name
        self.__total_sales = total_sales

    @property
    def cashier_id(self):
        return self.__cashier_id

    @property
    def empl_surname(self):
        return self.__empl_surname

    @property
    def empl_name(self):
        return self.__empl_name

    @property
    def total_sales(self):
        return self.__total_sales
