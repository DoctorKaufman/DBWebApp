class ReceiptExtDTO:
    def __init__(self, check_number, id_employee, card_number, c_percent, print_date, sum_total, vat):
        self.__check_number = check_number
        self.__id_employee = id_employee
        self.__card_number = card_number
        self.__c_percent = c_percent
        self.__print_date = print_date
        self.__sum_total = sum_total
        self.__vat = vat
        self.__products = []

    @property
    def check_number(self):
        return self.__check_number

    @property
    def id_employee(self):
        return self.__id_employee

    @property
    def card_number(self):
        return self.__card_number

    @property
    def c_percent(self):
        return self.__c_percent

    @property
    def print_date(self):
        return self.__print_date

    @property
    def sum_total(self):
        return self.__sum_total

    @property
    def vat(self):
        return self.__vat

    @property
    def products(self):
        return self.__products

    def set_sales_info(self, info_list):
        self.__products = info_list

    def serialize(self):
        card_reduction = 0
        if self.c_percent is not None:
            card_reduction = float(self.sum_total) - float(self.vat)
            card_reduction = card_reduction * float(self.c_percent) / (100.0 - float(self.c_percent))
        return {
            'Check_Num': self.check_number,
            'Employee_ID': self.id_employee,
            'Customer_Card': self.card_number,
            'Percent': float(0 if self.c_percent is None else self.c_percent),
            'Card_Reduction': card_reduction,
            'Print_Date': str(self.print_date),
            'Sum_Total': str(self.sum_total),
            'Vat': str(self.vat),
            'Products': [p.serialize() for p in self.products]
        }
