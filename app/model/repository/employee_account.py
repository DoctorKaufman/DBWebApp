import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.employee_account import EmployeeAccountDTO


class EmployeeAccountRepository:
    """
    Repository class for managing employee accounts in the database.
    """

    INSERT_EMPLOYEE_ACCOUNT_QUERY = sql.SQL("INSERT INTO employee_account (login, id_employee, password_hash) "
                                            "VALUES (%s, %s, %s)")
    UPDATE_EMPLOYEE_ACCOUNT_PASSWORD_QUERY = sql.SQL("UPDATE employee_account SET password_hash = %s WHERE login = %s")
    DELETE_EMPLOYEE_ACCOUNT_QUERY = sql.SQL("DELETE FROM employee_account WHERE login = %s")
    SELECT_EMPLOYEE_ACCOUNT_BY_LOGIN_QUERY = sql.SQL("SELECT * FROM employee_account WHERE login = %s")

    def __init__(self, conn):
        """
        Initialize EmployeeAccountRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def insert_employee_account(self, employee_account):
        """
        Insert a new employee account into the database.

        Parameters:
            employee_account: EmployeeAccountDTO object representing the employee account to insert.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeAccountRepository.INSERT_EMPLOYEE_ACCOUNT_QUERY,
                           (employee_account.login, employee_account.id_employee, employee_account.password_hash))
            self.conn.commit()

    def update_employee_account_password(self, login, new_password_hash):
        """
        Update an employee account's password in the database.

        Parameters:
            login: Login of the employee account to update.
            new_password_hash: New password hash to set for the employee account.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeAccountRepository.UPDATE_EMPLOYEE_ACCOUNT_PASSWORD_QUERY,
                           (new_password_hash, login))
            self.conn.commit()

    def delete_employee_account(self, login):
        """
        Delete an employee account from the database.

        Parameters:
            login: Login of the employee account to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(EmployeeAccountRepository.DELETE_EMPLOYEE_ACCOUNT_QUERY, (login,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_employee_account_by_login(self, login):
        """
        Retrieve an employee account by its login from the database.

        Parameters:
            login: Login of the employee account to retrieve.

        Returns:
            EmployeeAccountDTO object representing the retrieved employee account, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(EmployeeAccountRepository.SELECT_EMPLOYEE_ACCOUNT_BY_LOGIN_QUERY, (login,))
            employee_account_data = cursor.fetchone()
        if employee_account_data:
            return EmployeeAccountDTO(*employee_account_data)
        return None
