import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.receipt import ReceiptDTO


class ReceiptRepository:
    """
    Repository class for managing receipts in the database.
    """

    SELECT_ALL_RECEIPTS_QUERY = sql.SQL("SELECT * FROM receipt ORDER BY %s")
    SELECT_RECEIPT_QUERY = sql.SQL("SELECT * FROM receipt WHERE check_number = %s")
    INSERT_RECEIPT_QUERY = sql.SQL("INSERT INTO receipt (id_employee, card_number, print_date, sum_total, vat) "
                                   "VALUES (%s, %s, %s, %s, %s) RETURNING check_number")
    DELETE_RECEIPT_QUERY = sql.SQL("DELETE FROM receipt WHERE check_number = %s")
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

    def __init__(self, conn, sorting_column="check_number"):
        """
        Initialize ReceiptRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_receipts(self, sorting_column="check_number"):
        """
        Select all receipts from the database.

        Returns:
            Tuple of ReceiptDTO objects representing receipts.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ReceiptRepository.SELECT_ALL_RECEIPTS_QUERY, (sorting_column,))
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
