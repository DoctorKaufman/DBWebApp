class ReceiptDTO:
    def __init__(self, check_number, id_employee, card_number, print_date, sum_total, vat):
        self.__check_number = check_number
        self.__id_employee = id_employee
        self.__card_number = card_number
        self.__print_date = print_date
        self.__sum_total = sum_total
        self.__vat = vat

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
    def print_date(self):
        return self.__print_date

    @property
    def sum_total(self):
        return self.__sum_total

    @property
    def vat(self):
        return self.__vat
