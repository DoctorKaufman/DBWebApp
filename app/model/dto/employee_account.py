class EmployeeAccountDTO:
    def __init__(self, login, id_employee, password_hash):
        self.__login = login
        self.__id_employee = id_employee
        self.__password_hash = password_hash

    @property
    def login(self):
        return self.__login

    @property
    def id_employee(self):
        return self.__id_employee

    @property
    def password_hash(self):
        return self.__password_hash
