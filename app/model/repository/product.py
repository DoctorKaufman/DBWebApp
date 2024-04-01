import psycopg2
from psycopg2 import sql
from app.model.dto.product import ProductDTO


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_products(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM product")
        cursor.execute(query)
        products = []
        for product_data in cursor.fetchall():
            products.append(ProductDTO(product_data[0], product_data[1], product_data[2], product_data[3]))
        cursor.close()
        return tuple(products)

    def select_product(self, id_product):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM product WHERE id_product = %s")
        cursor.execute(query, (id_product,))
        product_data = cursor.fetchone()
        cursor.close()
        if product_data:
            return ProductDTO(product_data[0], product_data[1], product_data[2], product_data[3])
        return None

    """def insert_product(self, product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO product (id_product, category_number, product_name, p_characteristics) "
                        "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (product.id_product, product.category_number, product.product_name,
                               product.p_characteristics))
        self.conn.commit()
        cursor.close()"""

    def insert_product(self, product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO product (category_number, product_name, p_characteristics) "
                        "VALUES (%s, %s, %s) RETURNING id_product")
        cursor.execute(query, (product.category_number, product.product_name, product.p_characteristics))
        id_product = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if id_product:
            return ProductDTO(id_product, product.category_number, product.product_name, product.p_characteristics)
        return None

    def update_product(self, product):
        cursor = self.conn.cursor()
        query = sql.SQL("UPDATE product SET category_number = %s, product_name = %s, p_characteristics = %s "
                        "WHERE id_product = %s")
        cursor.execute(query, (product.category_number, product.product_name, product.p_characteristics, product.id_product))
        self.conn.commit()
        cursor.close()

    def delete_product(self, id_product):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM product WHERE id_product = %s")
        cursor.execute(query, (id_product,))
        self.conn.commit()
        cursor.close()

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
                        "WHERE cols.table_name = 'product'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
