class EmployeeAccountCreation:
    def __init__(self, login, password_hash, id_employee):
        self.__login = login
        self.__password_hash = password_hash
        self.__id_employee = id_employee

    @property
    def login(self):
        return self.__login

    @property
    def password_hash(self):
        return self.__password_hash

    @property
    def id_employee(self):
        return self.__id_employee
