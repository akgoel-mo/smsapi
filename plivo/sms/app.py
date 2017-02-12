import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from plivo.sms.config.provider import ConfigProvider


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigProvider().getPostGresConfig().get('url')
    app.config['REDIS_URL'] = ConfigProvider().getRedisConfig().get('url')
    return app

app = create_app()
app.logger.info("Creating application with ENV: {0}".format(str(ConfigProvider().getEnv())))
redis_store = FlaskRedis()
redis_store.init_app(app)
db = SQLAlchemy(app)


if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
