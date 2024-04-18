class RegistrationDTO:
    def __init__(self, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start,
                 phone_number, city, street, zip_code, login, password):
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
        self.__login = login
        self.__password = password

    @staticmethod
    def deserialize(data):
        return RegistrationDTO(data.get('empl_surname'), data.get('empl_name'),
                               data.get('empl_patronymic'), data.get('empl_role'), data.get('salary'),
                               data.get('date_of_birth'), data.get('date_of_start'), data.get('phone_number'),
                               data.get('city'), data.get('street'), data.get('zip_code'), data.get('login'),
                               data.get('password'))
