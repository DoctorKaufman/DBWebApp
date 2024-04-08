import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.customer_card import CustomerCardDTO


class CustomerCardRepository:
    """
    Repository class for managing customer cards in the database.
    """

    SELECT_ALL_CUSTOMER_CARDS_QUERY = sql.SQL("SELECT * FROM customer_card ORDER BY {} {}")
    SELECT_CUSTOMER_CARD_QUERY = sql.SQL("SELECT * FROM customer_card WHERE card_number = %s")
    INSERT_CUSTOMER_CARD_QUERY = sql.SQL("INSERT INTO customer_card (cust_surname, cust_name, cust_patronymic, "
                                         "phone_number, city, street, zip_code, c_percent) "
                                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING card_number")
    DELETE_CUSTOMER_CARD_QUERY = sql.SQL("DELETE FROM customer_card WHERE card_number = %s")
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
                                     "WHERE cols.table_name = 'customer_card'")

    def __init__(self, conn):
        """
        Initialize CustomerCardRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_customer_cards(self, pageable):
        """
        Select all customer cards from the database.

        Returns:
            Tuple of CustomerCardDTO objects representing customer cards.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerCardRepository.SELECT_ALL_CUSTOMER_CARDS_QUERY.format(sql.Identifier(pageable.column),
                                                                                         sql.SQL(pageable.order)))
            customer_cards = [CustomerCardDTO(*customer_card_data) for customer_card_data in cursor.fetchall()]
        return tuple(customer_cards)

    def select_customer_card(self, card_number):
        """
        Select a customer card by its card number.

        Parameters:
            card_number: Card number to select.

        Returns:
            CustomerCardDTO object representing the selected customer card, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerCardRepository.SELECT_CUSTOMER_CARD_QUERY, (card_number,))
            customer_card_data = cursor.fetchone()
        if customer_card_data:
            return CustomerCardDTO(*customer_card_data)
        return None

    def insert_customer_card(self, customer_card):
        """
        Insert a new customer card into the database.

        Parameters:
            customer_card: CustomerCardDTO object representing the customer card to insert.

        Returns:
            CustomerCardDTO object representing the inserted customer card, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerCardRepository.INSERT_CUSTOMER_CARD_QUERY,
                           (customer_card.cust_surname, customer_card.cust_name,
                            customer_card.cust_patronymic, customer_card.phone_number,
                            customer_card.city, customer_card.street,
                            customer_card.zip_code, customer_card.c_percent))
            card_number = cursor.fetchone()[0]
            self.conn.commit()
        if card_number:
            return CustomerCardDTO(card_number, customer_card.cust_surname, customer_card.cust_name,
                                   customer_card.cust_patronymic, customer_card.phone_number, customer_card.city,
                                   customer_card.street, customer_card.zip_code, customer_card.c_percent)
        return None

    def delete_customer_card(self, card_number):
        """
        Delete a customer card from the database.

        Parameters:
            card_number: Card number to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(CustomerCardRepository.DELETE_CUSTOMER_CARD_QUERY, (card_number,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_column_names(self):
        """
        Get column names of the 'customer_card' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerCardRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info
