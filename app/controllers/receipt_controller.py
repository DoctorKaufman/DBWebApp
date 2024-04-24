import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
from app.controllers.dtos.Pageable import Pageable
from app.controllers.mapper.mapper import ReceiptMapper
from app.model.repository.receipt import ReceiptRepository
from app.model.repository.sale import SaleRepository
from app.services.receipt_service import ReceiptService

receipt = Blueprint('receipt', __name__, url_prefix='/receipt')

receipt_repository = ReceiptRepository(get_connection())
sales_repository = SaleRepository(get_connection())

receipt_service = ReceiptService(receipt_repository, sales_repository)


@receipt.route('/', methods=['POST'])
def add_receipt():
    return ''


@receipt.route('/columns', methods=['GET'])
def get_columns():
    return json.dumps(receipt_service.get_receipt_columns())


@receipt.route('/', methods=['GET'])
def get_all_receipts():
    args = request.args
    receipts = receipt_service.get_all_receipts(Pageable.get_pageable(args, ReceiptMapper))
    return json.dumps([r.serialize() for r in receipts]), 200
