from flask import Flask

from plivo.sms.config.provider import ConfigProvider


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigProvider().getPostGresConfig().get('url')
    app.config['REDIS_URL'] = ConfigProvider().getRedisConfig().get('url')
    return app

app = create_app()
app.logger.info("Creating application with ENV: {0}".format(str(ConfigProvider().getEnv())))