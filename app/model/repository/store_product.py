import psycopg2
from psycopg2 import sql
from app.model.dto.store_product import StoreProductDTO


class StoreProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_store_products(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM store_product")
        cursor.execute(query)
        store_products = []
        for store_product_data in cursor.fetchall():
            store_products.append(StoreProductDTO(store_product_data[0], store_product_data[1],
                                                  store_product_data[2], store_product_data[3],
                                                  store_product_data[4], store_product_data[5]))
        cursor.close()
        return tuple(store_products)

    def select_store_product(self, upc):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM store_product WHERE UPC = %s")
        cursor.execute(query, (upc,))
        store_product_data = cursor.fetchone()
        cursor.close()
        if store_product_data:
            return StoreProductDTO(store_product_data[0], store_product_data[1], store_product_data[2],
                                   store_product_data[3], store_product_data[4], store_product_data[5])
        return None

    '''def insert_store_product(self, store_product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO store_product (UPC, UPC_prom, id_product, selling_price, products_number, "
                        "promotional_product) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (store_product.upc, store_product.upc_prom, store_product.id_product,
                               store_product.selling_price, store_product.products_number,
                               store_product.promotional_product))
        self.conn.commit()
        cursor.close()'''

    def insert_store_product(self, store_product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO store_product (UPC_prom, id_product, selling_price, products_number, "
                        "promotional_product) "
                        "VALUES (%s, %s, %s, %s, %s) RETURNING UPC, UPC_prom, id_product, selling_price, "
                        "products_number, promotional_product")
        cursor.execute(query, (store_product.UPC_prom, store_product.id_product,
                               store_product.selling_price, store_product.products_number,
                               store_product.promotional_product))
        upc = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if upc:
            return StoreProductDTO(upc[0], store_product.UPC_prom, store_product.id_product,
                                   store_product.selling_price, store_product.products_number,
                                   store_product.promotional_product)
        return None

    def delete_store_product(self, upc):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM store_product WHERE UPC = %s")
        cursor.execute(query, (upc,))
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
                        "WHERE cols.table_name = 'store_product'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
