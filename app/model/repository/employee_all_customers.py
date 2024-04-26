
from psycopg2 import sql

from app.model.dto.employee_all_customers import EmployeeAllCustomersDTO


class EmployeeAllCustomersRepository:
    EMPLOYEE_QUERY = sql.SQL("""
        SELECT e.id_employee, 
        e.empl_name AS employee_name, 
        e.empl_surname AS employee_surname
        FROM Employee e
        WHERE NOT EXISTS (
            SELECT * 
            FROM Customer_Card cc
            WHERE NOT EXISTS (
                SELECT *
                FROM Receipt r
                WHERE r.card_number = cc.card_number
                    AND r.id_employee = e.id_employee
            )
        );
    """)

    def __init__(self, conn):
        self.conn = conn

    def get_employees(self):
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeAllCustomersRepository.EMPLOYEE_QUERY)
            rows = cursor.fetchall()
            employees = []
            for row in rows:
                employee = EmployeeAllCustomersDTO(*row)
                employees.append(employee)
        return tuple(employees)

