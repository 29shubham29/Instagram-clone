import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from elasticsearch import Elasticsearch
from flask import Blueprint
from flask_moment import Moment
from celery import Celery

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

def create_app(config_class=Config):
    print("app created")
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    print(app.config['CELERY_BROKER_URL'])
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    celery.conf.update(app.config)
    # print(app.config['ELASTICSEARCH_URL'],app.config['CELERY_BROKER_URL'])

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
           if not os.path.exists('logs'):
               os.mkdir('logs')
           file_handler = RotatingFileHandler('logs/instagram.log', maxBytes=10240,backupCount=10)
           file_handler.setFormatter(logging.Formatter(
               '%(asctime)s %(levelname)s: %(message)s '
               '[in %(pathname)s:%(lineno)d]'))
           file_handler.setLevel(logging.INFO)
           app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('instagram')
    return app

from app import  models