import os
import settings


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dywe8y8oru92u389ru0i23hr823y8'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    UPLOAD_FOLDER = settings.UPLOAD_FOLDER


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
