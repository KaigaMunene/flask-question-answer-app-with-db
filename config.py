from distutils.debug import DEBUG
from pickle import TRUE


# the configurations for apps functionality


class Config:
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB = "flask_database.db"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB = "test.db"
