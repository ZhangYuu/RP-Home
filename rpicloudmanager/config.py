import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = BASEDIR + '/db/rpi.db'
    SECRET_KEY = os.urandom(24)
    USERNAME = 'admin'
    PASSWORD = 'default'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 2000


class Development(Config):
    pass


class Production(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 8080
