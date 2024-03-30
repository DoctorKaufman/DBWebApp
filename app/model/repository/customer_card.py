import psycopg2
from psycopg2 import sql
from app.model.dto.customer_card import CustomerCardDTO


class CustomerCardRepository:
    def __init__(self, conn):
        self.conn = conn

    def insert_customer_card(self, customer_card):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO Customer_Card (card_number, cust_surname, cust_name, cust_patronymic, "
                        "phone_number, city, street, zip_code, c_percent) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (customer_card.card_number, customer_card.cust_surname, customer_card.cust_name,
                               customer_card.cust_patronymic, customer_card.phone_number, customer_card.city,
                               customer_card.street, customer_card.zip_code, customer_card.c_percent))
        self.conn.commit()
        cursor.close()

    def select_customer_card(self, card_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Customer_Card WHERE card_number = %s")
        cursor.execute(query, (card_number,))
        customer_card_data = cursor.fetchone()
        cursor.close()
        if customer_card_data:
            return CustomerCardDTO(customer_card_data[0], customer_card_data[1], customer_card_data[2],
                                   customer_card_data[3], customer_card_data[4], customer_card_data[5],
                                   customer_card_data[6], customer_card_data[7], customer_card_data[8])
        return None

    def delete_customer_card(self, card_number):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM Customer_Card WHERE card_number = %s")
        cursor.execute(query, (card_number,))
        self.conn.commit()
        cursor.close()

    def select_all_customer_cards(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM Customer_Card")
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