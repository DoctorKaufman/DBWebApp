import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction
from app.model.dto.receipt import ReceiptDTO


class ReceiptRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_receipts(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM receipt")
        cursor.execute(query)
        receipts = []
        for receipt_data in cursor.fetchall():
            receipts.append(ReceiptDTO(receipt_data[0], receipt_data[1], receipt_data[2], receipt_data[3],
                                       receipt_data[4], receipt_data[5]))
        cursor.close()
        return tuple(receipts)

    def select_receipt(self, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM receipt WHERE check_number = %s")
        cursor.execute(query, (check_number,))
        receipt_data = cursor.fetchone()
        cursor.close()
        if receipt_data:
            return ReceiptDTO(receipt_data[0], receipt_data[1], receipt_data[2], receipt_data[3],
                              receipt_data[4], receipt_data[5])
        return None

    """def insert_receipt(self, receipt):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Receipt (check_number, id_employee, card_number, print_date, sum_total, vat) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (receipt.check_number, receipt.id_employee, receipt.card_number,
                               receipt.print_date, receipt.sum_total, receipt.vat))
        self.conn.commit()
        cursor.close()"""

    def insert_receipt(self, receipt):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO receipt (id_employee, card_number, print_date, sum_total, vat) "
                        "VALUES (%s, %s, %s, %s, %s) RETURNING check_number")
        cursor.execute(query, (receipt.id_employee, receipt.card_number, receipt.print_date,
                               receipt.sum_total, receipt.vat))
        check_number = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if check_number:
            return ReceiptDTO(check_number, receipt.id_employee, receipt.card_number, receipt.print_date,
                              receipt.sum_total, receipt.vat)
        return None

    def delete_receipt(self, check_number):
        cursor = self.conn.cursor()
        try:
            query = sql.SQL("DELETE FROM receipt WHERE check_number = %s")
            cursor.execute(query, (check_number,))
            self.conn.commit()
            cursor.close()
        except InFailedSqlTransaction as e:
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
                        "WHERE cols.table_name = 'receipt'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
