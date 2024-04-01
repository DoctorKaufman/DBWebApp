from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.category_input import CategoryInputDTO
from app.model.repository.category import CategoryRepository
from app.services.category_service import CategoryService

category = Blueprint('category', __name__, url_prefix='/category')

category_repository = CategoryRepository(get_connection())
category_service = CategoryService(category_repository)


@category.route('/', methods=['POST'])
def create_category():
    category_dto = CategoryInputDTO.deserialize(request.get_json())
    return category_service.create_category(category_dto).serialize(), 201


@category.route('/<int:category_number>/', methods=['PUT'])
def update_category(category_number):
    category_dto = CategoryInputDTO.deserialize(request.get_json())
    return category_service.update_category(category_dto, category_number).serialize(), 200


@category.route('/<int:category_id>/', methods=['DELETE'])
def delete_category(category_id):
    category_service.delete_category(category_id)
    return '', 204


@category.route('/<int:category_id>/', methods=['GET'])
def get_category(category_id):
    return category_service.get_by_category_number(category_id).serialize(), 200


@category.route('/', methods=['GET'])
def get_all_categories():
    categories = category_service.get_all_categories()
    return [c.serialize() for c in categories], 200


@category.route('/columns', methods=['GET'])
def get_columns():
    return category_service.get_category_columns()
