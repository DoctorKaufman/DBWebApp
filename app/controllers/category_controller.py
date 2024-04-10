import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.dtos.create.category_creation import CategoryCreationDTO
from app.controllers.mapper.mapper import CategoryMapper
from app.model.repository.category import CategoryRepository
from app.services.category_service import CategoryService

category = Blueprint('category', __name__, url_prefix='/category')

category_repository = CategoryRepository(get_connection())
category_service = CategoryService(category_repository)


@category.route('/', methods=['POST'])
def create_category():
    category_dto = CategoryCreationDTO.deserialize(request.get_json())
    return json.dumps(category_service.create_category(category_dto).serialize()), 201


@category.route('/<int:category_number>/', methods=['PUT'])
def update_category(category_number):
    category_dto = CategoryCreationDTO.deserialize(request.get_json())
    return json.dumps(category_service.update_category(category_dto, category_number).serialize()), 200


@category.route('/<int:category_id>/', methods=['DELETE'])
def delete_category(category_id):
    if category_service.delete_category(category_id):
        return '', 204
    return 'Could not delete category', 400


@category.route('/<int:category_id>/', methods=['GET'])
def get_category(category_id):
    return json.dumps(category_service.get_by_category_number(category_id).serialize()), 200


@category.route('/', methods=['GET'])
def get_all_categories():
    args = request.args
    categories = category_service.get_all_categories(Pageable.get_pageable(args, CategoryMapper))
    return json.dumps([c.serialize() for c in categories]), 200


@category.route('/columns', methods=['GET'])
def get_columns():
    return json.dumps(category_service.get_category_columns()), 200


@category.route('/droplist', methods=['GET'])
def get_drop_list():
    drop_list = category_service.get_drop_list()
    return json.dumps([c.serialize() for c in drop_list]), 200


@category.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(CategoryMapper.map_to_front_column(category_service.get_pk_name())), 200
