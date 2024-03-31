from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.product_input import ProductInputDTO
from app.model.repository.product import ProductRepository
from app.services.product_service import ProductService

product = Blueprint('product', __name__, url_prefix='/product')

product_repository = ProductRepository(get_connection())
product_service = ProductService(product_repository)


@product.route('/', methods=['POST'])
def create_product():
    product_dto = ProductInputDTO.deserialize(request.get_json())
    return product_service.create_product(product_dto).serialize(), 201


@product.route('/<int:id_product>/', methods=['PUT'])
def update_product(id_product):
    product_dto = ProductInputDTO.deserialize(request.get_json())
    return product_service.update_product(product_dto, id_product).serialize(), 200


@product.route('/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    product_service.delete_product(product_id)
    return '', 204


@product.route('/<int:product_id>', methods=["GET"])
def get_product(product_id):
    return product_service.get_product_by_id(product_id).serialize()


@product.route('/', methods=['GET'])
def get_all_products():
    products = product_service.get_all_products()
    return [p.serialize() for p in products], 200
