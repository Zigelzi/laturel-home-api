import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Defult production config
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv(f'DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

class DevConfig(Config):
    # Development config with debugging enabled
    DEBUG = True