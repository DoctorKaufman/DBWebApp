from flask import Flask

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)

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
    app.register_blueprint(main_blueprint)

    # Optionally, initialize Flask extensions like Flask-Login, Flask-Migrate, etc.

    return app
