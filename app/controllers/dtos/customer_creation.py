class CustomerCreationDTO:
    def __init__(self, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent):
        self.__cust_surname = cust_surname
        self.__cust_name = cust_name
        self.__cust_patronymic = cust_patronymic
        self.__phone_number = phone_number
        self.__city = city
        self.__street = street
        self.__zip_code = zip_code
        self.__c_percent = c_percent

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

    @staticmethod
    def deserialize(data):
        cust_surname = data['cust_surname']
        cust_name = data['cust_name']
        cust_patronymic = data['cust_patronymic']
        phone_number = data['phone_number']
        city = data['city']
        street = data['street']
        zip_code = data['zip_code']
        c_percent = float(data['c_percent'])
        return CustomerCreationDTO(cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent)
