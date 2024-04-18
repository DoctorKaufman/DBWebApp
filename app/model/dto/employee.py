class EmployeeDTO:
    def __init__(self, id_employee, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code):
        self.__id_employee = id_employee
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
    def id_employee(self):
        return self.__id_employee

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

    def serialize(self):
        return {
            'ID': self.__id_employee,
            'Name': self.__empl_name,
            'Surname': self.__empl_surname,
            'Patronymic': self.__empl_patronymic,
            'Role': self.__empl_role,
            'Salary': str(self.__salary),
            'Birth Date': str(self.__date_of_birth),
            'Start Date': str(self.__date_of_start),
            'Phone Number': self.__phone_number,
            'City': self.__city,
            'Street': self.__street,
            'Zip Code': self.__zip_code
        }
