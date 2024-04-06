import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.employee import EmployeeDTO


class EmployeeRepository:
    """
    Repository class for managing employees in the database.
    """

    SELECT_ALL_EMPLOYEES_QUERY = sql.SQL("SELECT * FROM employee ORDER BY id_employee")
    SELECT_EMPLOYEE_QUERY = sql.SQL("SELECT * FROM employee WHERE id_employee = %s")
    INSERT_EMPLOYEE_QUERY = sql.SQL("INSERT INTO employee (empl_surname, empl_name, empl_patronymic, empl_role, "
                                    "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_employee")
    DELETE_EMPLOYEE_QUERY = sql.SQL("DELETE FROM employee WHERE id_employee = %s")
    GET_COLUMN_NAMES_QUERY = sql.SQL("SELECT cols.column_name, "
                                     "CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN FALSE ELSE TRUE END "
                                     "FROM information_schema.columns AS cols "
                                     "LEFT JOIN information_schema.key_column_usage AS pkuse "
                                     "ON cols.table_schema = pkuse.constraint_schema "
                                     "AND cols.table_name = pkuse.table_name "
                                     "AND cols.column_name = pkuse.column_name "
                                     "LEFT JOIN information_schema.table_constraints AS tc "
                                     "ON pkuse.constraint_schema = tc.constraint_schema "
                                     "AND pkuse.constraint_name = tc.constraint_name "
                                     "WHERE cols.table_name = 'employee'")

    def __init__(self, conn):
        """
        Initialize EmployeeRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_employees(self):
        """
        Select all employees from the database.

        Returns:
            Tuple of EmployeeDTO objects representing employees.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.SELECT_ALL_EMPLOYEES_QUERY)
            employees = [EmployeeDTO(*employee_data) for employee_data in cursor.fetchall()]
        return tuple(employees)

    def select_employee(self, id_employee):
        """
        Select an employee by their employee ID.

        Parameters:
            id_employee: Employee ID to select.

        Returns:
            EmployeeDTO object representing the selected employee, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.SELECT_EMPLOYEE_QUERY, (id_employee,))
            employee_data = cursor.fetchone()
        if employee_data:
            return EmployeeDTO(*employee_data)
        return None

    def insert_employee(self, employee):
        """
        Insert a new employee into the database.

        Parameters:
            employee: EmployeeDTO object representing the employee to insert.

        Returns:
            EmployeeDTO object representing the inserted employee, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.INSERT_EMPLOYEE_QUERY, (employee.empl_surname, employee.empl_name,
                                                                      employee.empl_patronymic, employee.empl_role,
                                                                      employee.salary, employee.date_of_birth,
                                                                      employee.date_of_start, employee.phone_number,
                                                                      employee.city, employee.street,
                                                                      employee.zip_code))
            id_employee = cursor.fetchone()[0]
            self.conn.commit()
        if id_employee:
            return EmployeeDTO(id_employee, employee.empl_surname, employee.empl_name, employee.empl_patronymic,
                               employee.empl_role, employee.salary, employee.date_of_birth, employee.date_of_start,
                               employee.phone_number, employee.city, employee.street, employee.zip_code)
        return None

    def delete_employee(self, id_employee):
        """
        Delete an employee from the database.

        Parameters:
            id_employee: Employee ID to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(EmployeeRepository.DELETE_EMPLOYEE_QUERY, (id_employee,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_column_names(self):
        """
        Get column names of the 'employee' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info
