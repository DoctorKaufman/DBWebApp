from collections import OrderedDict

from app.controllers.handler.exceptions import DataDuplicateException
from app.model.dto.category import CategoryDTO
from app.services.enum.column_type import ColumnType


class CategoryService:
    def __init__(self, category_repository):
        self.category_repository = category_repository

        self.column_mapping = {
            'category_number': 'ID',
            'category_name': 'Name'
        }

    def get_by_category_number(self, category_number):
        return self.category_repository.select_category(category_number)

    def get_all_categories(self, pageable):
        return self.category_repository.select_all_categories(pageable)

    def create_category(self, category_creation_dto):
        # check for duplicate and process
        if self.category_repository.exists_category(category_creation_dto.category_name):
            raise DataDuplicateException("Category with such name already exists")
        return self.category_repository.insert_category(category_creation_dto)

    def update_category(self, category_dto, category_number):
        if self.category_repository.exists_category(category_dto.category_name):
            raise DataDuplicateException("Category with such name already exists")
        updated_category = CategoryDTO(category_number, category_dto.category_name)
        self.category_repository.update_category(updated_category)
        return updated_category

    def delete_category(self, category_number):
        return self.category_repository.delete_category(category_number)

    def get_category_columns(self):
        columns = self.category_repository.get_column_names()
        prettier_column = ColumnType.map_columns(columns, self.column_mapping)
        return OrderedDict(sorted(prettier_column.items(), key=lambda item: len(item[0])))

    def get_category_names(self):
        return self.category_repository.get_names()
