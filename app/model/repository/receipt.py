import psycopg2
from psycopg2 import sql
from app.model.dto.receipt import ReceiptDTO


class ReceiptRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_receipts(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Receipt")
        cursor.execute(query)
        receipts = []
        for receipt_data in cursor.fetchall():
            receipts.append(ReceiptDTO(receipt_data[0], receipt_data[1], receipt_data[2], receipt_data[3],
                                       receipt_data[4], receipt_data[5]))
        cursor.close()
        return tuple(receipts)

    def select_receipt(self, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Receipt WHERE check_number = %s")
        cursor.execute(query, (check_number,))
        receipt_data = cursor.fetchone()
        cursor.close()
        if receipt_data:
            return ReceiptDTO(receipt_data[0], receipt_data[1], receipt_data[2], receipt_data[3],
                              receipt_data[4], receipt_data[5])
        return None

    def insert_receipt(self, receipt):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Receipt (check_number, id_employee, card_number, print_date, sum_total, vat) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (receipt.check_number, receipt.id_employee, receipt.card_number,
                               receipt.print_date, receipt.sum_total, receipt.vat))
        self.conn.commit()
        cursor.close()

    def delete_receipt(self, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM Receipt WHERE check_number = %s")
        cursor.execute(query, (check_number,))
        self.conn.commit()
        cursor.close()
