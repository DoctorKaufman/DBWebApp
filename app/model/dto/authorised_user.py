class AuthorisedUserDTO:
    def __init__(self, id, username, position):
        self.__id = id
        self.__username = username
        self.__position = position

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def position(self):
        return self.__position

    def serialize(self):
        return {
            'id': self.__id,
            'username': self.__username,
            'position': self.__position
        }
