class CustomerDTO:
    def __init__(self, card_number, cust_surname, cust_name, phone_number,
                 total_purchases, total_amount_spent, average_purchase_amount, most_common_product_UPC,
                 most_common_product_name):
        self.__card_number = card_number
        self.__cust_surname = cust_surname
        self.__cust_name = cust_name
        self.__phone_number = phone_number
        self.__total_purchases = total_purchases
        self.__total_amount_spent = total_amount_spent
        self.__average_purchase_amount = average_purchase_amount
        self.__most_common_product_UPC = most_common_product_UPC
        self.__most_common_product_name = most_common_product_name

    @property
    def card_number(self):
        return self.__card_number

    @property
    def cust_surname(self):
        return self.__cust_surname

    @property
    def cust_name(self):
        return self.__cust_name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def total_purchases(self):
        return self.__total_purchases

    @property
    def total_amount_spent(self):
        return self.__total_amount_spent

    @property
    def average_purchase_amount(self):
        return self.__average_purchase_amount

    @property
    def most_common_product_UPC(self):
        return self.__most_common_product_UPC

    @property
    def most_common_product_name(self):
        return self.__most_common_product_name

    def serialize(self):
        return {'Card_Num': self.card_number,
                'Surname': self.cust_surname,
                'Name': self.cust_name,
                'Phone_Num': self.phone_number,
                'Total_Purchases': int(self.total_purchases),
                'Total_Spent': float(self.total_amount_spent),
                'Average_Purchase': float(self.average_purchase_amount),
                'Most_Common_UPC': self.most_common_product_UPC,
                'Most_Common_Product': self.most_common_product_name
                }
