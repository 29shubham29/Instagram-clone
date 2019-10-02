import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    LOG_TO_STDOUT=1
    REDIS_HOST = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_URL = 'redis://localhost:6379/0'

celery_test={
    'schedule-name':{
        'task':'app.routes.test',
    },
}