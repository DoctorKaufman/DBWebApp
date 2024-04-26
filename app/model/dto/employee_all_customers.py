class EmployeeAllCustomersDTO:
    def __init__(self, id_employee, employee_name, employee_surname):
        self.__id_employee = id_employee
        self.__employee_name = employee_name
        self.__employee_surname = employee_surname

    @property
    def id_employee(self):
        return self.__id_employee

    @property
    def employee_name(self):
        return self.__employee_name

    @property
    def employee_surname(self):
        return self.__employee_surname

    def serialize(self):
        return {
            'ID': self.id_employee,
            'Name': self.employee_name,
            'Surname': self.employee_surname
        }
