import psycopg2
from psycopg2 import sql
from app.model.dto.customer_card import CustomerCardDTO


class CustomerCardRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_customer_cards(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM customer_card")
        cursor.execute(query)
        customer_cards = []
        for customer_card_data in cursor.fetchall():
            customer_cards.append(CustomerCardDTO(customer_card_data[0], customer_card_data[1],
                                                  customer_card_data[2], customer_card_data[3],
                                                  customer_card_data[4], customer_card_data[5],
                                                  customer_card_data[6], customer_card_data[7],
                                                  customer_card_data[8]))
        cursor.close()
        return tuple(customer_cards)

    def select_customer_card(self, card_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM customer_card WHERE card_number = %s")
        cursor.execute(query, (card_number,))
        customer_card_data = cursor.fetchone()
        cursor.close()
        if customer_card_data:
            return CustomerCardDTO(customer_card_data[0], customer_card_data[1], customer_card_data[2],
                                   customer_card_data[3], customer_card_data[4], customer_card_data[5],
                                   customer_card_data[6], customer_card_data[7], customer_card_data[8])
        return None

    """def insert_customer_card(self, customer_card):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO customer_card (card_number, cust_surname, cust_name, cust_patronymic, "
                        "phone_number, city, street, zip_code, c_percent) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (customer_card.card_number, customer_card.cust_surname, customer_card.cust_name,
                               customer_card.cust_patronymic, customer_card.phone_number, customer_card.city,
                               customer_card.street, customer_card.zip_code, customer_card.c_percent))
        self.conn.commit()
        cursor.close()"""

    def insert_customer_card(self, customer_card):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO customer_card (cust_surname, cust_name, cust_patronymic, phone_number, "
                        "city, street, zip_code, c_percent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                        "RETURNING card_number")
        cursor.execute(query, (customer_card.cust_surname, customer_card.cust_name, customer_card.cust_patronymic,
                               customer_card.phone_number, customer_card.city, customer_card.street,
                               customer_card.zip_code, customer_card.c_percent))
        card_number = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if card_number:
            return CustomerCardDTO(card_number, customer_card.cust_surname, customer_card.cust_name,
                                   customer_card.cust_patronymic, customer_card.phone_number, customer_card.city,
                                   customer_card.street, customer_card.zip_code, customer_card.c_percent)
        return None

    def delete_customer_card(self, card_number):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM customer_card WHERE card_number = %s")
        cursor.execute(query, (card_number,))
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
                        "WHERE cols.table_name = 'customer_card'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
