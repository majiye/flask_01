# coding=utf-8
import os,base64
import redis


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/gflask_01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = '/oxz/7k162x6X5bHoGIaguhFJG3zvDkg'
    SECRET_KEY = 'base64.b64encode(os.urandom(24))'

    #redis实例用到的参数
    REDIS_PORT = '6379'
    REDIS_HOST = '192.168.189.139'

    # session配置
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True # 设置签名加密

    # 扩展默认会有redis的地址信息
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400 * 2

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

