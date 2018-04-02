# -*- coding:utf-8 -*-
'''app db 蓝图日志的生成'''
from logging.handlers import RotatingFileHandler
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from ihome.api_1_0 import api  # 注册蓝图用
from flask_wtf import CSRFProtect
import redis
from config import Config
from flask_session import Session
from utils.commons import RegexConverter
db = SQLAlchemy()

# 其他模块使用redis_store操作redis
redis_store = None
'''
开发中使用DEBUG级别, 来输出丰富的调试信息.
发布时使用WARN以上级别, 来显示异常信息
log文件存满, 会自动叠加序号, 并产生新的log文件. 如果文件存满了, 就覆盖原先的文件
'''
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)
# 参数config_class接收配置文件的开发模式类 Developmentconfig Productionconfig
def create_appdb(config_class):
    # 创建应用
    # 创建Flask类的实例， 即WIGS应用程序
    app = Flask(__name__)
    # 将自定义转换器添加到转换器字典中 必须放到路由前面
    app.url_map.converters['re'] = RegexConverter

    # db = SQLAlchemy(app)
    #调用数据库的配置
    app.config.from_object(config_class)
    # 惰性加载app
    db.init_app(app)

    # CSRF保护 针对post/put/delete等会修改数据的请求，需要开启保护
    CSRFProtect(app)

    # 创建redis
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
    # 利用扩展flask_session 创建session  保存浏览器的cookie session
    Session(app)


    # 蓝图的导入, 可以用到时在加载, 以避免循环导入的问题
    # 注册路由蓝图
    from ihome.api_1_0 import api  # 注册蓝图用
    app.register_blueprint(api)
    # 注册静态文件的蓝图
    import web_html
    app.register_blueprint(web_html.html)

    return app,db
