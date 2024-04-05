import psycopg2
from psycopg2 import sql
from app.model.dto.employee_account import EmployeeAccountDTO


class EmployeeAccountRepository:
    def __init__(self, conn):
        self.conn = conn

    def insert_employee_account(self, employee_account):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO employee_account (login, id_employee, password_hash) "
                        "VALUES (%s, %s, %s)")
        cursor.execute(query, (employee_account.login, employee_account.id_employee, employee_account.password_hash))
        self.conn.commit()
        cursor.close()

    def update_employee_account_password(self, login, new_password_hash):
        cursor = self.conn.cursor()
        query = sql.SQL("UPDATE employee_account SET password_hash = %s WHERE login = %s")
        cursor.execute(query, (new_password_hash, login))
        self.conn.commit()
        cursor.close()

    def delete_employee_account(self, login):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM employee_account WHERE login = %s")
        cursor.execute(query, (login,))
        self.conn.commit()
        cursor.close()

    def get_employee_account_by_login(self, login):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM employee_account WHERE login = %s")
        cursor.execute(query, (login,))
        employee_account_data = cursor.fetchone()
        cursor.close()
        if employee_account_data:
            return EmployeeAccountDTO(*employee_account_data)
        return None
