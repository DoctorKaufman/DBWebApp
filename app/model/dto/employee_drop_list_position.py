class EmployeeDropListPositionDTO:
    def __init__(self, id_employee, empl_surname):
        self.__id_employee = id_employee
        self.__empl_surname = empl_surname

    @property
    def id_employee(self):
        return self.__id_employee

    @property
    def empl_surname(self):
        return self.__empl_surname

