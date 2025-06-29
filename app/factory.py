from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_mail import Mail
from healthcheck import HealthCheck
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config

import os
import logging
from .celery_utils import init_celery

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(app_name=PKG_NAME, **kwargs):
  logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

  app = Flask(app_name)
  app.config.from_object(Config)

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
  from app.api import api_bp
  app.register_blueprint(api_bp, url_prefix='/api')

  SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
  API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

  # Call factory function to create our blueprint
  swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Flask API Base"
    }
   )

  app.register_blueprint(swaggerui_blueprint)

  
  # register health check
  health = HealthCheck()
  app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())


  # register models (to be picked by flask migrate command)
  from app.models.user import User
  from app.models.feature import Feature
  from app.models.role import Role
  from app.models.feature_role import FeatureRole

  return app