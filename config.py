from decouple import config
from flask_sqlalchemy import SQLAlchemy

class Config():
    SECRET_KEY = config('SECRET_KEY')
    
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD= config('MAIL_PASSWORD')
    SESSION_TYPE = 'filesystem'
    CONSUMER_KEY = config('CONSUMER_KEY')
    CONSUMER_SECRET = config('CONSUMER_SECRET')
    PASSKEY = config('PASSKEY')
    NGROK_ENDPOINT = config('NGROK_ENDPOINT')




class TestConfig():
    pass

class ProdConfig():
    pass
