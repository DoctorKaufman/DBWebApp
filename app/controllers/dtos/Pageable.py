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

    @staticmethod
    def get_pageable(args, mapper):
        db_column = mapper.map_to_db_column(args.get('sort', 'ID', type=str))
        return Pageable(db_column, args.get('order', 'asc', type=str))
    