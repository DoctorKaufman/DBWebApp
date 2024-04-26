import json

from flask import Blueprint, request
from app.controllers.connector.db_connector import get_connection
<<<<<<< HEAD
from app.model.repository.category_in_stock import CategoryInStockRepository
from app.model.repository.customer import CustomerRepository
=======
from app.model.repository.category_total_cost import CategoryTotalCostRepository
from app.model.repository.employee_all_customers import EmployeeAllCustomersRepository
>>>>>>> af7b1e6a4225cfc88dc8096acfcfd767d0624f02
from app.services.custom_query_service import CustomQueryService

query = Blueprint('query', __name__, url_prefix='/query')

<<<<<<< HEAD
customer_repository = CustomerRepository(get_connection())
category_repository = CategoryInStockRepository(get_connection())

customer_service = CustomQueryService(customer_repository, category_repository)
=======
category_repository = CategoryTotalCostRepository(get_connection())
employee_repository = EmployeeAllCustomersRepository(get_connection())

custom_service = CustomQueryService(category_repository, employee_repository)
>>>>>>> af7b1e6a4225cfc88dc8096acfcfd767d0624f02


@query.route('/1', methods=['GET'])
def get_customers():
    args = request.args
<<<<<<< HEAD
    min_amount = float(args['value'])
    return json.dumps([c.serialize() for c in customer_service.get_customers_statistics(min_amount)])
=======
    given_number = float(args['given_number'])
    return json.dumps([c.serialize() for c in custom_service.get_category_total_cost(given_number)])
>>>>>>> af7b1e6a4225cfc88dc8096acfcfd767d0624f02


@query.route('/2', methods=['GET'])
def get_categories():
<<<<<<< HEAD
    return json.dumps([c.serialize() for c in customer_service.get_categories_in_stock()])
=======
    return json.dumps([c.serialize() for c in custom_service.get_employees()])
>>>>>>> af7b1e6a4225cfc88dc8096acfcfd767d0624f02
