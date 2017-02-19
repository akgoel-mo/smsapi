import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify

from plivo.sms.config.provider import ConfigProvider


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigProvider().getPostGresConfig().get('url')
    app.config['REDIS_URL'] = ConfigProvider().getRedisConfig().get('url')
    # Configure application logger here
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
    return app


def http_error(e):
    return jsonify(dict(error=e.description, message=e.message)), e.code


def generic_error(e):
    app.logger.exception("unknown failure")
    return jsonify(dict(error='unknown failure', message=e.message)), 500


app = create_app()
app.logger.info("Creating application with ENV: {0}".format(str(ConfigProvider().getEnv())))
app.register_error_handler(405, http_error)
app.register_error_handler(401, http_error)
app.register_error_handler(403, http_error)
app.register_error_handler(Exception, generic_error)


def register_blueprints():
    from plivo.sms.resource import sms_blueprint
    app.register_blueprint(sms_blueprint)

register_blueprints()


if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
