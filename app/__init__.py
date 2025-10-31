from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger

from app.config import Config
from app.utils.logger import setup_logger

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    limiter.init_app(app)
    
    # 配置 Swagger
    swagger_config = {
        "headers": [],
        "specs": [{
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
    Swagger(app, config=swagger_config)
    
    # 设置日志
    setup_logger(app)
    
    # 注册蓝图
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
