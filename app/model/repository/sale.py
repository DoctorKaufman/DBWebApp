import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation

from app.model.dto.product_receipt import ProductReceiptDTO
from app.model.dto.sale import SaleDTO


class SaleRepository:
    """
    Repository class for managing sales in the database.
    """

    SELECT_SALE_QUERY = sql.SQL("SELECT * FROM sale WHERE UPC = %s AND check_number = %s")
    SELECT_CHECK_SALES_QUERY = sql.SQL("SELECT * FROM sale WHERE check_number = %s")
    SELECT_CHECK_SALES_QUERY_EXT = sql.SQL("SELECT product_name, sale.product_number, sale.selling_price FROM sale "
                                           "INNER JOIN store_product sp on sp.upc = sale.upc "
                                           "INNER JOIN product p on p.id_product = sp.id_product "
                                           "WHERE check_number = %s")
    SELECT_ALL_SALES_QUERY = sql.SQL("SELECT * FROM sale")
    INSERT_SALE_QUERY = sql.SQL("INSERT INTO sale (UPC, check_number, product_number, selling_price) "
                                "VALUES (%s, %s, %s, %s)")
    DELETE_SALE_QUERY = sql.SQL("DELETE FROM sale WHERE UPC = %s AND check_number = %s")
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
                                     "WHERE cols.table_name = 'sale'")

    def __init__(self, conn):
        """
        Initialize SaleRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_sale(self, upc, check_number):
        """
        Select a sale by its UPC and check number.

        Parameters:
            upc: UPC of the sale.
            check_number: Check number of the sale.

        Returns:
            SaleDTO object representing the selected sale, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.SELECT_SALE_QUERY, (upc, check_number))
            sale_data = cursor.fetchone()
        if sale_data:
            return SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3])
        return None

    def select_check_sales(self, check_number):
        """
        Select sales pack by their check number.

        Parameters:
            check_number: Check number of the sale.

        Returns:
            SaleDTO objects tuple representing the selected sales, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.SELECT_CHECK_SALES_QUERY, (check_number,))
            sales = [SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3]) for sale_data in cursor.fetchall()]
        return tuple(sales)

    def select_check_sale_ext(self, check_number):
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.SELECT_CHECK_SALES_QUERY_EXT, (check_number,))
            sales = [ProductReceiptDTO(sale_data[0], sale_data[1], sale_data[2]) for sale_data in cursor.fetchall()]
        return tuple(sales)

    def select_all_sales(self):
        """
        Select all sales from the database.

        Returns:
            Tuple of SaleDTO objects representing sales.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.SELECT_ALL_SALES_QUERY)
            sales = [SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3]) for sale_data in cursor.fetchall()]
        return tuple(sales)

    def insert_sale(self, sale):
        """
        Insert a new sale into the database.

        Parameters:
            sale: SaleDTO object representing the sale to insert.

        Returns:
            SaleDTO object representing the inserted sale, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.INSERT_SALE_QUERY,
                           (sale.upc, sale.check_number, sale.product_number, sale.selling_price))
            # sale_data = cursor.fetchone()
            self.conn.commit()
        # if sale_data:
        #     return SaleDTO(sale_data[0], sale_data[1], sale_data[2], sale_data[3])
        return None

    def delete_sale(self, upc, check_number):
        """
        Delete a sale from the database.

        Parameters:
            upc: UPC of the sale to delete.
            check_number: Check number of the sale to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(SaleRepository.DELETE_SALE_QUERY, (upc, check_number))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_column_names(self):
        """
        Get column names of the 'sale' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(SaleRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info
