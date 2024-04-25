import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable, SearchPageable
from app.controllers.dtos.create.check_creation import ReceiptCreationDTO
from app.controllers.mapper.mapper import ReceiptMapper
from app.model.dto import receipts_input
from app.model.repository.customer_card import CustomerCardRepository
from app.model.repository.receipt import ReceiptRepository
from app.model.repository.sale import SaleRepository
from app.model.repository.store_product import StoreProductRepository
from app.services.receipt_service import ReceiptService
from app.services.store_product_service import StoreProductService

receipt = Blueprint('receipt', __name__, url_prefix='/receipt')

receipt_repository = ReceiptRepository(get_connection())
sales_repository = SaleRepository(get_connection())
store_product_repository = StoreProductRepository(get_connection())
customer_card_repository = CustomerCardRepository(get_connection())

receipt_service = ReceiptService(receipt_repository, sales_repository, store_product_repository,
                                 customer_card_repository)

store_product_repository = StoreProductRepository(get_connection())
store_product_service = StoreProductService(store_product_repository)


# @receipt.route('/', methods=['POST'])
# def add_receipt():
#     return ''


@receipt.route('/', methods=['GET'])
def get_all_receipts():
    args = request.args
    receipts = receipt_service.get_all_receipts(Pageable.get_pageable(args, ReceiptMapper))
    return json.dumps([r.serialize() for r in receipts]), 200


@receipt.route('/<int:check_num>', methods=['GET'])
def get_receipt(check_num):
    return json.dumps(receipt_service.select_by_check_num(check_num).serialize())


@receipt.route('/statistic', methods=['GET'])
def get_receipt_statistic():
    args = request.args
    statistic_pageable = SearchPageable.get_pageable(args)
    receipts = receipt_service.get_all_receipts_with_condition(statistic_pageable)
    return json.dumps([r.serialize() for r in receipts]), 200


@receipt.route('/sum', methods=['GET'])
def get_receipt_sum():
    args = request.args
    sum_pageable = SearchPageable.get_pageable(args)
    return {'sum': receipt_service.get_sum_of_checks_period(sum_pageable)}


@receipt.route('/product', methods=["GET"])
def get_sum():
    args = request.args
    return {
        'Total Sales':
            store_product_service.get_sales_of_product(SearchPageable.get_pageable(args))
    }


@receipt.route('/', methods=['POST'])
def create_receipt():
    receipt_dto = ReceiptCreationDTO.deserialize(request.get_json())
    receipt_service.create_receipt(receipt_dto)
    return '', 201


@receipt.route('/<int:check_num>', methods=['DELETE'])
def delete_receipt(check_num):
    receipt_service.delete_receipt(check_num)
    return '', 204
