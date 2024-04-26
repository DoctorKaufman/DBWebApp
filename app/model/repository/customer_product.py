from psycopg2 import sql

from app.model.dto.customer_product import CustomerCardProductDTO


class CustomerCardProductRepository:
    CUSTOMER_CARD_PRODUCT_QUERY = sql.SQL("""
        SELECT cc.card_number,
                cc.cust_surname,
                cc.cust_name,
                cc.cust_patronymic
        FROM Customer_Card cc
        WHERE NOT EXISTS (
            SELECT pc.id_product
            FROM Product pc
            WHERE pc.category_number = %s
            AND NOT EXISTS (
                SELECT s.UPC
                FROM Sale s
                JOIN Store_Product sp ON s.UPC = sp.UPC
                WHERE sp.id_product = pc.id_product
                AND s.check_number IN (
                    SELECT r.check_number
                    FROM Receipt r
                    WHERE r.card_number = cc.card_number
                )
            )
        );
    """)

    def __init__(self, conn):
        self.conn = conn

    def get_customer_card_products(self, category_number):
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerCardProductRepository.CUSTOMER_CARD_PRODUCT_QUERY, (category_number,))
            rows = cursor.fetchall()
            cards = []
            for row in rows:
                card = CustomerCardProductDTO(*row)
                cards.append(card)
        return tuple(cards)

