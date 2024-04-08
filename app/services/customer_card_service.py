class CustomerService:
    def __init__(self, customer_card_repository):
        self.customer_card_repository = customer_card_repository

    def get_customer_card_by_card_number(self, card_number):
        return self.customer_card_repository.select_customer_card(card_number)

    def get_all_customer_cards(self, sort_column):
        return self.customer_card_repository.select_all_customer_cards(sort_column)

    def create_customer_card(self, customer_dto):
        return self.customer_card_repository.insert_customer_card(customer_dto)

    def delete_customer_card(self, card_number):
        self.customer_card_repository.delete_customer_card(card_number)

    def get_customer_columns(self):
        return self.customer_card_repository.get_column_names()
