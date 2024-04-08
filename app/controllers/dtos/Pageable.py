class Pageable:
    def __init__(self, column, order):
        self.__column = column
        self.__order = order
        
    @property
    def column(self):
        return self.__column
    
    @property
    def order(self):
        return self.__order
    