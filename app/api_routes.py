from flask import Blueprint

# Create the API blueprint
api_bp = Blueprint("api", __name__)

# Import all controllers to register their routes
from app.controllers.api.v1 import auth_controller, files_controller, users_controller  # noqa: F401, E402
