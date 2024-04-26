class CustomerCardProductDTO:
    def __init__(self, card_number, cust_surname, cust_name, cust_patronymic):
        self.__card_number = card_number
        self.__cust_surname = cust_surname
        self.__cust_name = cust_name
        self.__cust_patronymic = cust_patronymic

    @property
    def card_number(self):
        return self.__card_number

    @property
    def cust_surname(self):
        return self.__cust_surname

    @property
    def cust_name(self):
        return self.__cust_name

    @property
    def cust_patronymic(self):
        return self.__cust_patronymic

    def serialize(self):
        return {
            'Card_Num': self.__card_number,
            'Surname': self.__cust_surname,
            'Name': self.__cust_name,
            'Patronymic': self.__cust_patronymic
        }
