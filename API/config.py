import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
     
    #TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    #TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    #twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


    #def fetch_sms():
    #   return DevelopmentConfig.twilio_api.messages.stream()


class TestingConfig(BaseConfig):
    pass