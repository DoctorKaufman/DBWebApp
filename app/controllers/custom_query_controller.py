import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
from app.model.repository.category_in_stock import CategoryInStockRepository
from app.model.repository.customer import CustomerRepository
from app.services.custom_query_service import CustomQueryService

query = Blueprint('query', __name__, url_prefix='/query')

customer_repository = CustomerRepository(get_connection())
category_repository = CategoryInStockRepository(get_connection())

customer_service = CustomQueryService(customer_repository, category_repository)


@query.route('/1', methods=['GET'])
def get_customers():
    args = request.args
    min_amount = float(args['min-amount'])
    return json.dumps([c.serialize() for c in customer_service.get_customers_statistics(min_amount)])


@query.route('/2', methods=['GET'])
def get_categories():
    return json.dumps([c.serialize() for c in customer_service.get_categories_in_stock()])
