import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation

from app.model.dto.cashier_sales import CashierSalesDTO
from app.model.dto.receipt import ReceiptDTO
from app.model.dto.receipt_ext import ReceiptExtDTO


class ReceiptRepository:
    """
    Repository class for managing receipts in the database.
    """

    SELECT_ALL_RECEIPTS_QUERY = sql.SQL("SELECT * FROM receipt ORDER BY {} {}")
    SELECT_ALL_RECEIPTS_QUERY_EXT = sql.SQL("SELECT check_number, id_employee, receipt.card_number, "
                                            "c.c_percent, print_date, sum_total, vat "
                                            "FROM receipt "
                                            "INNER JOIN customer_card c ON receipt.card_number = c.card_number "
                                            "ORDER BY {} {}")
    SELECT_RECEIPT_QUERY = sql.SQL("SELECT * FROM receipt WHERE check_number = %s")
    SELECT_RECEIPTS_FOR_PERIOD_QUERY = sql.SQL("SELECT * FROM receipt "
                                               "WHERE DATE(print_date) >= %s "
                                               "AND DATE(print_date) <= %s")
    SELECT_CASHIER_RECEIPTS_FOR_PERIOD_QUERY = sql.SQL("SELECT * FROM receipt "
                                                       "WHERE id_employee = %s "
                                                       "AND DATE(print_date) >= %s "
                                                       "AND DATE(print_date) <= %s ")
    INSERT_RECEIPT_QUERY = sql.SQL("INSERT INTO receipt (id_employee, card_number, print_date, sum_total, vat) "
                                   "VALUES (%s, %s, %s, %s, %s) RETURNING check_number")
    UPDATE_RECEIPT_QUERY = sql.SQL("UPDATE receipt SET id_employee = %s, card_number = %s, print_date = %s, "
                                   "sum_total = %s, vat = %s WHERE check_number = %s")
    DELETE_RECEIPT_QUERY = sql.SQL("DELETE FROM receipt WHERE check_number = %s")
    GET_CASHIER_SALES_PRICE = sql.SQL("SELECT e.id_employee, e.empl_surname, e.empl_name, "
                                      "COALESCE(SUM(r.sum_total), 0) AS total_sales "
                                      "FROM employee e "
                                      "LEFT JOIN receipt r ON e.id_employee = r.id_employee "
                                      "WHERE e.id_employee = %s "
                                      "AND DATE(r.print_date) >= %s "
                                      "AND DATE(r.print_date) <= %s "
                                      "GROUP BY e.id_employee, e.empl_surname, e.empl_name")
    GET_TOTAL_SALES = sql.SQL("SELECT COALESCE(SUM(sum_total), 0) AS total_sales "
                              "FROM receipt "
                              "WHERE DATE(print_date) >= %s AND DATE(print_date) <= %s")
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
                                     "WHERE cols.table_name = 'receipt'")
    GET_PRIMARY_KEY_NAME_QUERY = sql.SQL("SELECT cols.column_name FROM information_schema.columns AS cols "
                                         "JOIN information_schema.key_column_usage AS pkuse "
                                         "ON cols.table_schema = pkuse.constraint_schema "
                                         "AND cols.table_name = pkuse.table_name "
                                         "AND cols.column_name = pkuse.column_name "
                                         "JOIN information_schema.table_constraints AS tc "
                                         "ON pkuse.constraint_schema = tc.constraint_schema "
                                         "AND pkuse.constraint_name = tc.constraint_name "
                                         "WHERE cols.table_name = 'receipt' "
                                         "AND tc.constraint_type = 'PRIMARY KEY'")

    def __init__(self, conn, sorting_column="check_number"):
        """
        Initialize ReceiptRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_receipts(self, pageable):
        """
        Select all receipts from the database.

        Parameters:
            pageable: Pageable class object containing parameters for ordering.

        Returns:
            Tuple of ReceiptDTO objects representing receipts.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.SELECT_ALL_RECEIPTS_QUERY.format(sql.Identifier(pageable.column),
                                                                              sql.SQL(pageable.order)))
            receipts = [ReceiptDTO(*receipt_data) for receipt_data in cursor.fetchall()]
        return tuple(receipts)

    def select_all_receipts_ext(self, pageable):
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.SELECT_ALL_RECEIPTS_QUERY_EXT.format(sql.Identifier(pageable.column),
                                                                                  sql.SQL(pageable.order)))
            receipts = [ReceiptExtDTO(*receipt_data) for receipt_data in cursor.fetchall()]
        return tuple(receipts)

    def select_cashier_receipts(self, receipts_input):
        """
        Select cashier's receipts for a specified period of time from the database.

        Parameters:
            receipts_input: ReceiptsInputDTO class object containing parameters for ordering.

        Returns:
            Tuple of ReceiptDTO objects representing cashier's receipts for specified period.
        """
        with self.conn.cursor() as cursor:
            if receipts_input.cashier_id:
                cursor.execute(ReceiptRepository.SELECT_CASHIER_RECEIPTS_FOR_PERIOD_QUERY,
                               (receipts_input.cashier_id, receipts_input.start_date, receipts_input.end_date))
            else:
                cursor.execute(ReceiptRepository.SELECT_CASHIER_RECEIPTS_FOR_PERIOD_QUERY,
                               (receipts_input.start_date, receipts_input.end_date))
            receipts = [ReceiptDTO(*receipt_data) for receipt_data in cursor.fetchall()]
        return tuple(receipts)

    def select_receipt(self, check_number):
        """
        Select a receipt by its check number.

        Parameters:
            check_number: Check number of the receipt to select.

        Returns:
            ReceiptDTO object representing the selected receipt, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.SELECT_RECEIPT_QUERY, (check_number,))
            receipt_data = cursor.fetchone()
        if receipt_data:
            return ReceiptDTO(*receipt_data)
        return None

    def insert_receipt(self, receipt):
        """
        Insert a new receipt into the database.

        Parameters:
            receipt: ReceiptDTO object representing the receipt to insert.

        Returns:
            ReceiptDTO object representing the inserted receipt, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.INSERT_RECEIPT_QUERY,
                           (receipt.id_employee, receipt.card_number, receipt.print_date,
                            receipt.sum_total, receipt.vat))
            check_number = cursor.fetchone()[0]
            self.conn.commit()
        if check_number:
            return ReceiptDTO(check_number, receipt.id_employee, receipt.card_number, receipt.print_date,
                              receipt.sum_total, receipt.vat)
        return None

    def update_receipt(self, receipt):
        """
        Update an existing receipt in the database.

        Parameters:
            receipt: ReceiptDTO object representing the receipt to update.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.UPDATE_RECEIPT_QUERY,
                           (receipt.id_employee, receipt.card_number, receipt.print_date,
                            receipt.sum_total, receipt.vat, receipt.check_number))
            self.conn.commit()

    def delete_receipt(self, check_number):
        """
        Delete a receipt from the database.

        Parameters:
            check_number: Check number of the receipt to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(ReceiptRepository.DELETE_RECEIPT_QUERY, (check_number,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def calculate_total_sales_by_cashier(self, receipts_input):
        """
        Calculate the total sales amount of products from receipts created by a specific cashier within a specified
        time period.

        Parameters:
            receipts_input: ReceiptsInputDTO object containing the input data.

        Returns:
            CashierSalesDTO object representing the result.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.GET_CASHIER_SALES_PRICE,
                           (receipts_input.start_date, receipts_input.end_date, receipts_input.cashier_id))
            result = cursor.fetchone()
            if result:
                return CashierSalesDTO(result[0], result[1], result[2], result[3])
            else:
                return None

    def calculate_total_sales_all_cashiers(self, sales_input):
        """
        Calculate the total sales amount of products from receipts created by all cashiers within a specified time
        period.

        Parameters:
            sales_input: SalesInputDTO object containing the input data.

        Returns:
            Total sum of checks for the given period.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                
            """, (sales_input.start_date, sales_input.end_date))
            results = cursor.fetchone()
            return results

    def get_column_names(self):
        """
        Get column names of the 'receipt' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info

    def get_primary_key_name(self):
        """
        Get the name of the primary key column in the 'receipt' table.

        Returns:
            String representing the name of the primary key column, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.GET_PRIMARY_KEY_NAME_QUERY)
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
