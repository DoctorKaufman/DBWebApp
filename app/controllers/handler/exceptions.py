class DataDuplicateException(Exception):
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message


class ValidationException(Exception):
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message


class CheckCreationException(Exception):
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message
