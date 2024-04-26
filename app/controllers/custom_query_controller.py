import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
from app.model.repository.categoty_product_count import CategoryProductCountRepository
from app.model.repository.customer_product import CustomerCardProductRepository
from app.services.custom_query_service import CustomQueryService

query = Blueprint('query', __name__, url_prefix='/query')

category_repository = CategoryProductCountRepository(get_connection())
customer_repository = CustomerCardProductRepository(get_connection())

custom_service = CustomQueryService(category_repository, customer_repository)


@query.route('/1', methods=['GET'])
def get_customers():
    args = request.args
    category_number = int(args['category_number'])
    return json.dumps([c.serialize() for c in custom_service.get_customer_card_products(category_number)])


@query.route('/2', methods=['GET'])
def get_categories():
    return json.dumps([c.serialize() for c in custom_service.get_category_product_counts()])
