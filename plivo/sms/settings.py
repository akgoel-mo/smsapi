from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from plivo.sms.app import app

db = SQLAlchemy(app)
redis_store = FlaskRedis()
redis_store.init_app(app)
