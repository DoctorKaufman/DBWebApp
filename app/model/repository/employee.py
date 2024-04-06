import psycopg2
from psycopg2 import sql
from app.model.dto.employee import EmployeeDTO


class EmployeeRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_employees(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM employee")
        cursor.execute(query)
        employees = []
        for employee_data in cursor.fetchall():
            employees.append(EmployeeDTO(employee_data[0], employee_data[1], employee_data[2], employee_data[3],
                                         employee_data[4], employee_data[5], employee_data[6], employee_data[7],
                                         employee_data[8], employee_data[9], employee_data[10], employee_data[11]))
        cursor.close()
        return tuple(employees)

    def select_employee(self, id_employee):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM employee WHERE id_employee = %s")
        cursor.execute(query, (id_employee,))
        employee_data = cursor.fetchone()
        cursor.close()
        if employee_data:
            return EmployeeDTO(employee_data[0], employee_data[1], employee_data[2], employee_data[3],
                               employee_data[4], employee_data[5], employee_data[6], employee_data[7],
                               employee_data[8], employee_data[9], employee_data[10], employee_data[11])
        return None

    """def insert_employee(self, employee):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Employee (id_employee, empl_surname, empl_name, empl_patronymic, empl_role, "
                        "salary, date_of_birth, date_of_start, phone_number, city, street, zip_code) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (employee.id_employee, employee.empl_surname, employee.empl_name,
                               employee.empl_patronymic, employee.empl_role, employee.salary,
                               employee.date_of_birth, employee.date_of_start, employee.phone_number,
                               employee.city, employee.street, employee.zip_code))
        self.conn.commit()
        cursor.close()"""

    def insert_employee(self, employee):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO employee (empl_surname, empl_name, empl_patronymic, empl_role, salary, "
                        "date_of_birth, date_of_start, phone_number, city, street, zip_code) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_employee")
        cursor.execute(query, (employee.empl_surname, employee.empl_name, employee.empl_patronymic,
                               employee.empl_role, employee.salary, employee.date_of_birth, employee.date_of_start,
                               employee.phone_number, employee.city, employee.street, employee.zip_code))
        id_employee = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if id_employee:
            return EmployeeDTO(id_employee, employee.empl_surname, employee.empl_name, employee.empl_patronymic,
                               employee.empl_role, employee.salary, employee.date_of_birth, employee.date_of_start,
                               employee.phone_number, employee.city, employee.street, employee.zip_code)
        return None

    def delete_employee(self, id_employee):
        cursor = self.conn.cursor()
        try:
            query = sql.SQL("DELETE FROM employee WHERE id_employee = %s")
            cursor.execute(query, (id_employee,))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            cursor.close()
            return False
        finally:
            cursor.close()
        return True

    def get_column_names(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT cols.column_name, "
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
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
