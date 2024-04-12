import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.receipt import ReceiptDTO


class ReceiptRepository:
    """
    Repository class for managing receipts in the database.
    """

    SELECT_ALL_RECEIPTS_QUERY = sql.SQL("SELECT * FROM receipt ORDER BY {} {}")
    SELECT_RECEIPT_QUERY = sql.SQL("SELECT * FROM receipt WHERE check_number = %s")
    INSERT_RECEIPT_QUERY = sql.SQL("INSERT INTO receipt (id_employee, card_number, print_date, sum_total, vat) "
                                   "VALUES (%s, %s, %s, %s, %s) RETURNING check_number")
    UPDATE_RECEIPT_QUERY = sql.SQL("UPDATE receipt SET id_employee = %s, card_number = %s, print_date = %s, "
                                   "sum_total = %s, vat = %s WHERE check_number = %s")
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