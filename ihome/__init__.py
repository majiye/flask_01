# -*- coding:utf-8 -*-
'''app db 蓝图日志的生成'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from ihome.api_1_0 import api  # 注册蓝图用
from flask_wtf import CSRFProtect

db = SQLAlchemy()


# 参数config_class接收配置文件的开发模式类 Developmentconfig Productionconfig
def create_appdb(config_class):
    # 创建应用
    # 创建Flask类的实例， 即WIGS应用程序
    app = Flask(__name__)
    # 创建数据库

    # db = SQLAlchemy(app)
    #调用数据库的配置
    app.config.from_object(config_class)
    # 惰性加载app
    db.init_app(app)

    # CSRF保护 针对post/put/delete等会修改数据的请求，需要开启保护
    CSRFProtect(app)

    # 蓝图的导入, 可以用到时在加载, 以避免循环导入的问题
    # 注册蓝图
    from ihome.api_1_0 import api  # 注册蓝图用
    app.register_blueprint(api)
    return app,db
