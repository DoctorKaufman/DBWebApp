import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.employee import EmployeeDTO
from app.model.dto.employee_drop_list_position import EmployeeDropListPositionDTO


class EmployeeRepository:
    """
    Repository class for managing employees in the database.
    """

    SELECT_ALL_EMPLOYEES_QUERY = sql.SQL("SELECT * FROM employee ORDER BY {} {}")
    SEARCH_QUERY_TEMPLATE = sql.SQL("SELECT * FROM employee WHERE "
                                    "SIMILARITY({0}, %s) > 0.2 "
                                    "ORDER BY {1} {2}")
    SEARCH_QUERY_TEMPLATE_BY_COL = sql.SQL("SELECT * FROM employee WHERE "
                                    "{0} = %s "
                                    "ORDER BY {1} {2}")
    SELECT_EMPLOYEE_QUERY = sql.SQL("SELECT * FROM employee WHERE id_employee = %s")
    SELECT_EMPLOYEES_DROP_LIST_QUERY = sql.SQL("SELECT id_employee, empl_surname FROM employee")
    INSERT_EMPLOYEE_QUERY = sql.SQL("INSERT INTO employee (empl_surname, empl_name, empl_patronymic, empl_role, "
                                    "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_employee")
    UPDATE_EMPLOYEE_QUERY = sql.SQL("UPDATE employee SET empl_surname = %s, empl_name = %s, empl_patronymic = %s, "
                                    "empl_role = %s, salary = %s, date_of_birth = %s, date_of_start = %s, "
                                    "phone_number = %s, city = %s, street = %s, zip_code = %s "
                                    "WHERE id_employee = %s")
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
    GET_PRIMARY_KEY_NAME_QUERY = sql.SQL("SELECT cols.column_name FROM information_schema.columns AS cols "
                                         "JOIN information_schema.key_column_usage AS pkuse "
                                         "ON cols.table_schema = pkuse.constraint_schema "
                                         "AND cols.table_name = pkuse.table_name "
                                         "AND cols.column_name = pkuse.column_name "
                                         "JOIN information_schema.table_constraints AS tc "
                                         "ON pkuse.constraint_schema = tc.constraint_schema "
                                         "AND pkuse.constraint_name = tc.constraint_name "
                                         "WHERE cols.table_name = 'employee' "
                                         "AND tc.constraint_type = 'PRIMARY KEY'")

    non_string_columns = {'id_employee', 'salary', 'date_of_birth', 'date_of_start'}

    def __init__(self, conn):
        """
        Initialize EmployeeRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_employees(self, pageable):
        """
        Select all employees from the database.

        Parameters:
            pageable: Pageable class object containing parameters for ordering and search.

        Returns:
            Tuple of EmployeeDTO objects representing employees.
        """
        with self.conn.cursor() as cursor:
            if pageable.search_column and pageable.search_value:
                if pageable.search_column not in self.non_string_columns:
                    search_query = self.SEARCH_QUERY_TEMPLATE.format(
                        sql.Identifier(pageable.search_column),
                        sql.Identifier(pageable.column),
                        sql.SQL(pageable.order)
                    )
                    cursor.execute(search_query, (pageable.search_value,))
                else:
                    search_query = self.SEARCH_QUERY_TEMPLATE_BY_COL.format(
                        sql.Identifier(pageable.search_column),
                        sql.Identifier(pageable.column),
                        sql.SQL(pageable.order)
                    )
                    cursor.execute(search_query, (pageable.search_value,))
            else:
                cursor.execute(
                    EmployeeRepository.SELECT_ALL_EMPLOYEES_QUERY.format(
                        sql.Identifier(pageable.column),
                        sql.SQL(pageable.order))
                )

            employees = [EmployeeDTO(*employee_data) for employee_data in cursor.fetchall()]
        return tuple(employees)

    def select_employees_drop_list(self):
        """
        Select all employees from the database to form drop list

        Returns:
            Tuple of EmployeeDropListPositionDTO objects representing products
            drop list positions.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.SELECT_EMPLOYEES_DROP_LIST_QUERY)
            employee = [EmployeeDropListPositionDTO(employee_data[0], employee_data[1]) for employee_data in
                        cursor.fetchall()]
        return tuple(employee)

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

    def update_employee(self, employee):
        """
        Update an existing employee in the database.

        Parameters:
            employee: EmployeeDTO object representing the employee to update.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.UPDATE_EMPLOYEE_QUERY,
                           (employee.empl_surname, employee.empl_name, employee.empl_patronymic,
                            employee.empl_role, employee.salary, employee.date_of_birth,
                            employee.date_of_start, employee.phone_number, employee.city,
                            employee.street, employee.zip_code, employee.id_employee))
            self.conn.commit()

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

    def get_primary_key_name(self):
        """
        Get the name of the primary key column in the 'employee' table.

        Returns:
            String representing the name of the primary key column, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeRepository.GET_PRIMARY_KEY_NAME_QUERY)
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None