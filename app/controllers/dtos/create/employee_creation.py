from app.controllers.handler.exceptions import ValidationException
from app.controllers.utils.validation_utils import is_adult, validate_phone_number


class EmployeeCreationDTO:
    def __init__(self, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start,
                 phone_number, city, street, zip_code):
        self.__empl_surname = empl_surname
        self.__empl_name = empl_name
        self.__empl_patronymic = empl_patronymic
        self.__empl_role = empl_role
        self.__salary = salary
        self.__date_of_birth = date_of_birth
        self.__date_of_start = date_of_start
        self.__phone_number = phone_number
        self.__city = city
        self.__street = street
        self.__zip_code = zip_code

    @property
    def empl_surname(self):
        return self.__empl_surname

    @property
    def empl_name(self):
        return self.__empl_name

    @property
    def empl_patronymic(self):
        return self.__empl_patronymic

    @property
    def empl_role(self):
        return self.__empl_role

    @property
    def salary(self):
        return self.__salary

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def date_of_start(self):
        return self.__date_of_start

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

    @staticmethod
    def deserialize(data):
        salary = float(data.get('Salary'))
        if salary <= 0:
            raise ValidationException('Salary must be greater than zero')
        birth_date = data.get('Birth_Date')
        if not is_adult(birth_date):
            raise ValidationException('Employee age should be greater or equal to 18')
        phone_num = data.get('Phone_Number')
        if not validate_phone_number(phone_num):
            raise ValidationException('Phone number must be valid. Should contain 13 symbols (with +)')
        return EmployeeCreationDTO(data.get('Surname'), data.get('Name'),
                                   data.get('Patronymic'), data.get('Role'), data.get('Salary'),
                                   data.get('Birth_Date'), data.get('Start_Date'), data.get('Phone_Number'),
                                   data.get('City'), data.get('Street'), data.get('Zip'))
