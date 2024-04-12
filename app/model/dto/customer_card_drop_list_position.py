class CustomerCardDropListPositionDTO:
    def __init__(self, card_number, cust_surname):
        self.__card_number = card_number
        self.__cust_surname = cust_surname

    @property
    def card_number(self):
        return self.__card_number

    @property
    def cust_surname(self):
        return self.__cust_surname
