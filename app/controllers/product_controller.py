import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.dtos.create.product_creation import ProductCreationDTO
from app.controllers.mapper.mapper import ProductMapper
from app.model.repository.product import ProductRepository
from app.services.product_service import ProductService

product = Blueprint('product', __name__, url_prefix='/product')

product_repository = ProductRepository(get_connection())
product_service = ProductService(product_repository)


@product.route('/', methods=['POST'])
def create_product():
    product_dto = ProductCreationDTO.deserialize(request.get_json())
    return json.dumps(product_service.create_product(product_dto).serialize()), 201


@product.route('/<int:id_product>/', methods=['PUT'])
def update_product(id_product):
    product_dto = ProductCreationDTO.deserialize(request.get_json())
    return json.dumps(product_service.update_product(product_dto, id_product).serialize()), 200


@product.route('/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    successful = product_service.delete_product(product_id)
    if successful:
        return '', 204
    else:
        return '', 400


@product.route('/<int:product_id>', methods=["GET"])
def get_product(product_id):
    return json.dumps(product_service.get_product_by_id_product(product_id).serialize())


@product.route('/', methods=['GET'])
def get_all_products():
    args = request.args
    products = product_service.get_all_products(Pageable.get_pageable(args, ProductMapper))
    return json.dumps([p.serialize() for p in products]), 200


@product.route('/columns', methods=['GET'])
def get_columns():
    return json.dumps(product_service.get_product_columns())


@product.route('/droplist', methods=['GET'])
def get_drop_list():
    drop_list = product_service.get_drop_list()
    return json.dumps([c.serialize() for c in drop_list]), 200


@product.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(ProductMapper.map_to_front_column(product_service.get_pk_name())), 200
