import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable, SearchPageable
from app.controllers.dtos.create.store_product_creation import StoreProductCreationDTO
from app.controllers.mapper.mapper import StoreProductMapper
from app.model.repository.store_product import StoreProductRepository
from app.services.store_product_service import StoreProductService

store_product = Blueprint('store_product', __name__, url_prefix='/store-product')

store_product_repository = StoreProductRepository(get_connection())
store_product_service = StoreProductService(store_product_repository)


@store_product.route('/', methods=['POST'])
def create_store_product():
    store_product_dto = StoreProductCreationDTO.deserialize(request.get_json())
    return json.dumps(store_product_service.create_store_product(store_product_dto).serialize()), 201


@store_product.route('/<int:upc>', methods=["PUT"])
def update_store_product(upc):
    store_product_dto = StoreProductCreationDTO.deserialize(request.get_json())
    return json.dumps(store_product_service.update_store_product(upc, store_product_dto).serialize()), 200


@store_product.route('/<int:upc>', methods=['DELETE'])
def delete_store_product(upc):
    return json.dumps(store_product_service.delete_store_product(upc)), 200


@store_product.route('/<int:upc>', methods=['GET'])
def get_store_product(upc):
    return json.dumps(store_product_service.get_store_product_by_upc(upc).serialize()), 200


@store_product.route('/', methods=['GET'])
def get_all_store_products():
    args = request.args
    store_products = store_product_service.get_all_store_products(Pageable.get_pageable(args, StoreProductMapper))
    return json.dumps([p.serialize() for p in store_products]), 200


@store_product.route('/columns', methods=['GET'])
def get_columns():
    return json.dumps(store_product_service.get_store_product_columns())


@store_product.route('/droplist', methods=['GET'])
def get_drop_list():
    drop_list = store_product_service.get_drop_list()
    return json.dumps([c.serialize() for c in drop_list]), 200


@store_product.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(StoreProductMapper.map_to_front_column(store_product_service.get_pk_name())), 200
