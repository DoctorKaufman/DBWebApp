import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
from app.model.repository.category_total_cost import CategoryTotalCostRepository
from app.model.repository.employee_all_customers import EmployeeAllCustomersRepository
from app.services.custom_query_service import CustomQueryService

query = Blueprint('query', __name__, url_prefix='/query')

category_repository = CategoryTotalCostRepository(get_connection())
employee_repository = EmployeeAllCustomersRepository(get_connection())

custom_service = CustomQueryService(category_repository, employee_repository)


@query.route('/1', methods=['GET'])
def get_customers():
    args = request.args
    given_number = float(args['value'])
    return json.dumps([c.serialize() for c in custom_service.get_category_total_cost(given_number)])


@query.route('/2', methods=['GET'])
def get_categories():
    return json.dumps([c.serialize() for c in custom_service.get_employees()])
