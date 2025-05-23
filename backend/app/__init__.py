from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from flask_cors import CORS
from .config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from .models import db
from .auth import auth
from .routes import api
from .admin import init_admin


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=False)
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    Migrate(app, db)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
        # Опционально: кнопки Submit должны быть видны всегда
        "swagger_ui_config": {
            "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"]
        }
    }

    Swagger(
        app,
        config=swagger_config,
        template_file='docs/swagger.yml'
    )

    app.register_blueprint(api)
    if not app.config.get('TESTING'):
        init_admin(app)

    return app
