from app.controllers.handler.exceptions import DataDuplicateException
from app.controllers.mapper.mapper import CategoryMapper
from app.model.dto.category import CategoryDTO


class CategoryService:
    def __init__(self, category_repository):
        self.category_repository = category_repository

    def get_by_category_number(self, category_number):
        return self.category_repository.select_category(category_number)

    def get_all_categories(self, pageable):
        return self.category_repository.select_all_categories(pageable)

    def create_category(self, category_creation_dto):
        # check for duplicate and process
        if self.category_name_exists(category_creation_dto.category_name):
            raise DataDuplicateException("Category with such name already exists")
        return self.category_repository.insert_category(category_creation_dto)

    def update_category(self, category_dto, category_number):
        category_name = category_dto.category_name
        same_name_as_existing = (self.category_name_exists(category_name) and
                                 category_name != self.category_repository
                                 .select_category(category_number).category_name)
        if same_name_as_existing:
            raise DataDuplicateException("Category with such name already exists")
        updated_category = CategoryDTO(category_number, category_dto.category_name)
        self.category_repository.update_category(updated_category)
        return updated_category

    def delete_category(self, category_number):
        return self.category_repository.delete_category(category_number)

    def get_category_columns(self):
        return CategoryMapper.map_columns(self.category_repository.get_column_names())

    def get_category_names(self):
        return self.category_repository.get_names()

    def get_drop_list(self):
        return self.category_repository.select_categories_drop_list()

    def get_pk_name(self):
        return self.category_repository.get_primary_key_name()

    def category_name_exists(self, category_name):
        return self.category_repository.exists_category(category_name)
