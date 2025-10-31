from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.routes import captcha_routes, system_routes
