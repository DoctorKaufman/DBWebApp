import psycopg2
from psycopg2 import sql
from app.model.dto.product import ProductDTO


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_products(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Product")
        cursor.execute(query)
        products = []
        for product_data in cursor.fetchall():
            products.append(ProductDTO(product_data[0], product_data[1], product_data[2], product_data[3]))
        cursor.close()
        return tuple(products)

    def select_product(self, id_product):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Product WHERE id_product = %s")
        cursor.execute(query, (id_product,))
        product_data = cursor.fetchone()
        cursor.close()
        if product_data:
            return ProductDTO(product_data[0], product_data[1], product_data[2], product_data[3])
        return None

    """def insert_product(self, product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Product (id_product, category_number, product_name, p_characteristics) "
                        "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (product.id_product, product.category_number, product.product_name,
                               product.p_characteristics))
        self.conn.commit()
        cursor.close()"""

    def insert_product(self, product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Product (category_number, product_name, p_characteristics) "
                        "VALUES (%s, %s, %s) RETURNING id_product")
        cursor.execute(query, (product.category_number, product.product_name, product.p_characteristics))
        id_product = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if id_product:
            return ProductDTO(id_product, product.category_number, product.product_name, product.p_characteristics)
        return None

    def delete_product(self, id_product):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM Product WHERE id_product = %s")
        cursor.execute(query, (id_product,))
        self.conn.commit()
        cursor.close()
