import psycopg2
from psycopg2 import sql
from app.model.dto.store_product import StoreProductDTO


class StoreProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_store_products(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Store_Product")
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
        query = sql.SQL("SELECT * FROM Store_Product WHERE UPC = %s")
        cursor.execute(query, (upc,))
        store_product_data = cursor.fetchone()
        cursor.close()
        if store_product_data:
            return StoreProductDTO(store_product_data[0], store_product_data[1], store_product_data[2],
                                   store_product_data[3], store_product_data[4], store_product_data[5])
        return None

    def insert_store_product(self, store_product):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Store_Product (UPC, UPC_prom, id_product, selling_price, products_number, "
                        "promotional_product) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (store_product.upc, store_product.upc_prom, store_product.id_product,
                               store_product.selling_price, store_product.products_number,
                               store_product.promotional_product))
        self.conn.commit()
        cursor.close()

    def delete_store_product(self, upc):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM Store_Product WHERE UPC = %s")
        cursor.execute(query, (upc,))
        self.conn.commit()
        cursor.close()
