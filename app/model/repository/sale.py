import psycopg2
from psycopg2 import sql
from app.model.dto.sale import SaleDTO


class SaleRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_sale(self, upc, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Sale WHERE UPC = %s AND check_number = %s")
        cursor.execute(query, (upc, check_number))
        sale_data = cursor.fetchone()
        cursor.close()
        if sale_data:
            return SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3])
        return None

    def select_all_sales(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Sale")
        cursor.execute(query)
        sales = []
        for sale_data in cursor.fetchall():
            sales.append(SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3]))
        cursor.close()
        return tuple(sales)

    def insert_sale(self, sale):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Sale (UPC, check_number, product_number, selling_price) VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (sale.UPC, sale.check_number, sale.product_number, sale.selling_price))
        self.conn.commit()
        cursor.close()

    def delete_sale(self, upc, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM Sale WHERE UPC = %s AND check_number = %s")
        cursor.execute(query, (upc, check_number))
        self.conn.commit()
        cursor.close()
