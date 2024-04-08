import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.product import ProductDTO


class ProductRepository:
    """
    Repository class for managing products in the database.
    """

    SELECT_ALL_PRODUCTS_QUERY = sql.SQL("SELECT * FROM product ORDER BY {} {}")
    SELECT_PRODUCT_QUERY = sql.SQL("SELECT * FROM product WHERE id_product = %s")
    INSERT_PRODUCT_QUERY = sql.SQL("INSERT INTO product (category_number, product_name, p_characteristics) "
                                   "VALUES (%s, %s, %s) RETURNING id_product")
    UPDATE_PRODUCT_QUERY = sql.SQL("UPDATE product SET category_number = %s, product_name = %s, "
                                   "p_characteristics = %s WHERE id_product = %s")
    DELETE_PRODUCT_QUERY = sql.SQL("DELETE FROM product WHERE id_product = %s")
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
                                     "WHERE cols.table_name = 'product'")

    def __init__(self, conn):
        """
        Initialize ProductRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_products(self, pageable):
        """
        Select all products from the database.

        Returns:
            Tuple of ProductDTO objects representing products.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ProductRepository.SELECT_ALL_PRODUCTS_QUERY.format(sql.Identifier(pageable.column),
                                                                              sql.SQL(pageable.order)))
            products = [ProductDTO(*product_data) for product_data in cursor.fetchall()]
        return tuple(products)

    def select_product(self, id_product):
        """
        Select a product by its ID.

        Parameters:
            id_product: ID of the product to select.

        Returns:
            ProductDTO object representing the selected product, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ProductRepository.SELECT_PRODUCT_QUERY, (id_product,))
            product_data = cursor.fetchone()
        if product_data:
            return ProductDTO(*product_data)
        return None

    def insert_product(self, product):
        """
        Insert a new product into the database.

        Parameters:
            product: ProductDTO object representing the product to insert.

        Returns:
            ProductDTO object representing the inserted product, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ProductRepository.INSERT_PRODUCT_QUERY,
                           (product.category_number, product.product_name, product.p_characteristics))
            id_product = cursor.fetchone()[0]
            self.conn.commit()
        if id_product:
            return ProductDTO(id_product, product.category_number, product.product_name, product.p_characteristics)
        return None

    def update_product(self, product):
        """
        Update a product in the database.

        Parameters:
            product: ProductDTO object representing the product to update.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ProductRepository.UPDATE_PRODUCT_QUERY,
                           (product.category_number, product.product_name, product.p_characteristics,
                            product.id_product))
            self.conn.commit()

    def delete_product(self, id_product):
        """
        Delete a product from the database.

        Parameters:
            id_product: ID of the product to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(ProductRepository.DELETE_PRODUCT_QUERY, (id_product,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_column_names(self):
        """
        Get column names of the 'product' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(ProductRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info
