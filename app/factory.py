import logging
import os

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from healthcheck import HealthCheck

from config import Config

from .celery_utils import init_celery

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(app_name=PKG_NAME, config_override=None, **kwargs):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )

    app = Flask(app_name)

    # Apply base configuration
    app.config.from_object(Config)

    # Apply test configuration override if provided
    if config_override:
        app.config.update(config_override)

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    # register orm with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # register seed
    seeder = FlaskSeeder()
    seeder.init_app(app, db)

    # register routes
    from app.api_routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
    API_URL = "/static/swagger.json"  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={"app_name": "Flask API Base"},  # Swagger UI config overrides
    )

    app.register_blueprint(swaggerui_blueprint)

    # register health check
    health = HealthCheck()
    app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

    # register models (to be picked by flask migrate command)
    from app.models.feature import Feature  # noqa: F401
    from app.models.feature_role import FeatureRole  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.user import User  # noqa: F401

    return app
