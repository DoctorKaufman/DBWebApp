from app.controllers.dtos.create.product_buy_dto import ProductBuyDTO


class ReceiptCreationDTO:
    def __init__(self, id_employee, card_number, bought_products):
        self.__id_employee = id_employee
        self.__card_number = card_number
        self.__bought_products = bought_products

    @property
    def id_employee(self):
        return self.__id_employee

    @property
    def card_number(self):
        return self.__card_number

    @property
    def bought_products(self):
        return self.__bought_products

    @staticmethod
    def deserialize(data):
        products = data['products']
        deserialized_products = []
        for product in products:
            deserialized_products.append(ProductBuyDTO.deserialize(product))

        return ReceiptCreationDTO(data['id_employee'], data['card_number'], deserialized_products)
