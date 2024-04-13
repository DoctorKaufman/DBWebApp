from enum import Enum, auto


class ColumnType(Enum):
    PK = auto()  # Primary Key
    FK = auto()  # Foreign Key
    ATTRIB = auto()  # Attribute
    HIDDEN = auto()  # Hidden

    def serialize(self):
        """Serialize the Enum value to a string."""
        return self.name

    @staticmethod
    def map_columns(columns, column_map):
        prettier_column = {}
        for column_name, editable in columns.items():
            prettier_column_name = column_map.get(column_name, column_name)
            prettier_column[
                prettier_column_name] = ColumnType.ATTRIB.serialize() if editable else ColumnType.PK.serialize()
        return prettier_column
