# coding=utf-8
import os,base64
import redis
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/flask_01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = '/oxz/7k162x6X5bHoGIaguhFJG3zvDkg'
    SECRET_KEY = 'base64.b64encode(os.urandom(24))'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

