from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from app.controllers.custom_query_controller import query
from app.controllers.handler.exceptions import DataDuplicateException, ValidationException, CheckCreationException
from app.controllers.handler.error_handler import handle_data_duplicate_exception

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
# API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager()

    CORS(app)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    jwt.init_app(app)
    # Session(app)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=300)

    # Load configuration from 'config.py' file or parameter
    if config_filename is not None:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object('config.DefaultConfig')

    # Initialize database (if using Flask-SQLAlchemy for Models)

    # from .models import db
    # db.init_app(app)

    # Import and register Blueprints (for Controllers/Views)
    from .views.main import main as main_blueprint
    from .views.goods_and_categories import goods_and_categories as goods_and_categories_blueprint
    from .views.staff_and_clients import staff_and_clients as staff_and_clients_blueprint
    from .views.receipts import receipts as receiptsWC

    from app.controllers.employee_controller import employee
    from app.controllers.category_controller import category
    from app.controllers.product_controller import product
    from app.controllers.customer_card_controller import customer
    from app.controllers.check_controller import check
    from app.controllers.store_product_controller import store_product
    from app.controllers.authentication_controller import auth
    from app.controllers.receipt_controller import receipt

    app.register_blueprint(employee)
    app.register_blueprint(category)
    app.register_blueprint(product)
    app.register_blueprint(customer)
    app.register_blueprint(check)
    app.register_blueprint(store_product)
    app.register_blueprint(auth)
    app.register_blueprint(receipt)
    app.register_blueprint(query)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(goods_and_categories_blueprint, url_prefix='/goods-and-categories')
    app.register_blueprint(staff_and_clients_blueprint, url_prefix='/staff-and-clients')
    app.register_blueprint(receipts)

    app.context_processor(inject_user)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)

    # Optionally, initialize Flask extensions like Flask-Login, Flask-Migrate, etc.

    app.errorhandler(DataDuplicateException)(handle_data_duplicate_exception)
    app.errorhandler(ValidationException)(handle_data_duplicate_exception)
    app.errorhandler(CheckCreationException)(handle_data_duplicate_exception)
    return app


def inject_user():
    user = ''
    return dict(user=user)
