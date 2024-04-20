class StoreProductSalesDTO:
    def __init__(self, upc, product_name, total_quantity_sold):
        self.__upc = upc
        self.__product_name = product_name
        self.__total_quantity_sold = total_quantity_sold

    @property
    def upc(self):
        return self.__upc

    @property
    def product_name(self):
        return self.__product_name

    @property
    def total_quantity_sold(self):
        return self.__total_quantity_sold
