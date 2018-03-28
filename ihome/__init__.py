
'''app db 蓝图日志的生成'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 参数config_class接收配置文件的开发模式类 Developmentconfig Productionconfig
def create_appdb(config_class):
    # 创建应用
    # 创建Flask类的实例， 即WIGS应用程序
    app = Flask(__name__)
    # 创建数据库
    db = SQLAlchemy(app)
    #调用数据库的配置
    app.config.from_object(config_class)
    return app,db
