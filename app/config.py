import os

class Config:
    """应用配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 日志配置
    LOG_FILE = 'app.log'
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    
    # API配置
    MAX_BATCH_SIZE = 20
    DEFAULT_RATE_LIMIT = "30 per minute"
    
    # 服务器配置
    HOST = '::'
    PORT = 7777
    DEBUG = True
    THREADED = True
