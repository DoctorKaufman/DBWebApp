from app.controllers.handler.exceptions import ValidationException
from app.controllers.utils.validation_utils import validate_phone_number


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
        cust_name = data['Name']
        cust_surname = data['Surname']
        cust_patronymic = data['Patronymic']
        phone_number = data['PhoneNum']
        city = data['City']
        street = data['Street']
        zip_code = data['Zip']
        c_percent = float(data['Percent'])
        if cust_surname is None or cust_name is None or cust_patronymic is None or phone_number is None or city is None or street is None:
            raise ValidationException("Customer data can't be empty")
        if c_percent < 0:
            raise ValidationException("Percent can't be negative")
        if c_percent > 100:
            raise ValidationException("Percent can't be greater than 100")
        if not validate_phone_number(phone_number):
            raise ValidationException('Phone number must be valid. Should contain 13 symbols (with +)')
        return CustomerCreationDTO(cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent)
