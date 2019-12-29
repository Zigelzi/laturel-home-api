import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Defult production config
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.getenv('DB_NAME', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

class DevConfig(Config):
    # Development config with debugging enabled
    DEBUG = True