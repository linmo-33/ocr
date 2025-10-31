import logging

def setup_logger(app):
    """配置日志"""
    logging.basicConfig(
        filename=app.config['LOG_FILE'],
        level=getattr(logging, app.config['LOG_LEVEL']),
        format=app.config['LOG_FORMAT']
    )
    return app.logger
