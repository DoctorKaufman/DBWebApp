class PasswordDTO:
    def __init__(self, password):
        self.__password = password

    @property
    def password(self):
        return self.__password

    @staticmethod
    def deserialize(data):
        return PasswordDTO(data.get('Password'))
