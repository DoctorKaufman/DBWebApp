import json

from flask import Blueprint, request

from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.dtos.create.customer_creation import CustomerCreationDTO
from app.controllers.mapper.mapper import CustomerCardMapper
from app.model.repository.customer_card import CustomerCardRepository
from app.services.customer_card_service import CustomerService

customer = Blueprint('customer', __name__, url_prefix='/customer')

customer_card_repository = CustomerCardRepository(get_connection())
customer_service = CustomerService(customer_card_repository)


@customer.route('/', methods=['POST'])
def create_customer():
    customer_dto = CustomerCreationDTO.deserialize(request.get_json())
    return customer_service.create_customer_card(customer_dto).serialize(), 201


# @customer.route('/<int:card_number>/', methods=['PUT'])
# def update_customer(card_number):
#     return ''


@customer.route('/<int:card_number>/', methods=['DELETE'])
def delete_customer(card_number):
    customer_service.delete_customer_card(card_number)
    return '', 204


@customer.route('/<int:card_number>/', methods=['GET'])
def get_customer(card_number):
    return json.dumps(customer_service.get_customer_card_by_card_number(card_number).serialize()), 200


@customer.route('/', methods=['GET'])
def get_all_customers():
    args = request.args
    customers = customer_service.get_all_customer_cards(Pageable.get_pageable(args, CustomerCardMapper))
    return json.dumps([c.serialize() for c in customers]), 200


@customer.route('/columns', methods=['GET'])
def get_columns():
    return json.dumps(customer_service.get_customer_columns())


@customer.route('/pk', methods=['GET'])
def get_pk_name():
    return json.dumps(CustomerCardMapper.map_to_front_column(customer_service.get_pk_name())), 200
