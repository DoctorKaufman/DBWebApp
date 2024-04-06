import psycopg2
from psycopg2 import sql
from app.model.dto.sale import SaleDTO


class SaleRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_sale(self, upc, check_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM sale WHERE UPC = %s AND check_number = %s")
        cursor.execute(query, (upc, check_number))
        sale_data = cursor.fetchone()
        cursor.close()
        if sale_data:
            return SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3])
        return None

    def select_all_sales(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM sale")
        cursor.execute(query)
        sales = []
        for sale_data in cursor.fetchall():
            sales.append(SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3]))
        cursor.close()
        return tuple(sales)

    """def insert_sale(self, sale):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO sale (UPC, check_number, product_number, selling_price) VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (sale.UPC, sale.check_number, sale.product_number, sale.selling_price))
        self.conn.commit()
        cursor.close()"""

    def insert_sale(self, sale):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO sale (UPC, check_number, product_number, selling_price) "
                        "VALUES (%s, %s, %s, %s) RETURNING *")
        cursor.execute(query, (sale.UPC, sale.check_number, sale.product_number, sale.selling_price))
        sale_data = cursor.fetchone()
        self.conn.commit()
        cursor.close()
        if sale_data:
            return SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3])
        return None

    def delete_sale(self, upc, check_number):
        cursor = self.conn.cursor()
        try:
            query = sql.SQL("DELETE FROM sale WHERE UPC = %s AND check_number = %s")
            cursor.execute(query, (upc, check_number))
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
                        "WHERE cols.table_name = 'sale'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
