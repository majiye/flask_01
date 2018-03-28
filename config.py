# 项目的配置文档
import os
import redis
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/flask_01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#项目的调试模式
class ProductionConfig(Config):
    pass
# 项目的发布模式
class DevelopmentConfig(Config):
    DEBUG = True
    # 创建会话密钥
    SECRET_KEY = 'os.urandom(24)'