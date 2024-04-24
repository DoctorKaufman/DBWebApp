class ProductReceiptDTO:
    def __init__(self, product_name, product_number, product_price):
        self.__product_name = product_name
        self.__product_number = product_number
        self.__product_price = product_price

    @property
    def product_name(self):
        return self.__product_name

    @property
    def product_number(self):
        return self.__product_number

    @property
    def product_price(self):
        return self.__product_price

    def serialize(self):
        return {
            'Product_Name': self.product_name,
            'Product_Number': int(self.product_number),
            'Product_Price': float(self.product_price)
        }
