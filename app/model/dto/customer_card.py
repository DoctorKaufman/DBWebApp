class CustomerCardDTO:
    def __init__(self, card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code,
                 c_percent):
        self.__card_number = card_number
        self.__cust_surname = cust_surname
        self.__cust_name = cust_name
        self.__cust_patronymic = cust_patronymic
        self.__phone_number = phone_number
        self.__city = city
        self.__street = street
        self.__zip_code = zip_code
        self.__c_percent = c_percent

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

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def city(self):
        return self.__city

    @property
    def street(self):
        return self.__street

    @property
    def zip_code(self):
        return self.__zip_code

    @property
    def c_percent(self):
        return self.__c_percent

    def serialize(self):
        return {
            "ID": self.__card_number,
            "Surname": self.__cust_surname,
            "Name": self.__cust_name,
            "PhoneNum": self.__phone_number,
            "City": self.__city,
            "Street": self.__street,
            "ZipCode": self.__zip_code,
            "Percent": self.__c_percent
            # "card_number": self.__card_number,
            # "cust_surname": self.__cust_surname,
            # "cust_name": self.__cust_name,
            # "phone_number": self.__phone_number,
            # "city": self.__city,
            # "street": self.__street,
            # "zip_code": self.__zip_code,
            # "c_percent": self.__c_percent
        }
