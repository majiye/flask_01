# -*- coding:utf-8 -*-
'''主要负责程序的启动 以及 数据库的操作'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager  # 启动扩展包
from flask_migrate import Migrate, MigrateCommand  # 迁移命令扩展包
import os
import redis
from flask import blueprints
# 创建Flask类的实例， 即WIGS应用程序
app = Flask(__name__)
# 创建数据库
db = SQLAlchemy(app)

manager = Manager(app)
# 迁移操作 第一个参数是flask实例 第二个参数是SQLALchemy实例
migrate = Migrate(app, db)
# 对数据库增加可迁移操作命令
manager.add_command('db', MigrateCommand)
#调用数据库的配置
# 注册蓝图

'''项目的配置'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/flask_01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 创建会话密钥
SECRET_KEY = 'os.urandom(24)'


# 函数create_appdb的参数 可以控制项目是调试模式 还是发布模式


#创建蓝图
api = blueprints('api',__name__)
app.register_blueprint(api)

@api.route('/')
def index():
    return 'Hello World'


# lask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    # app.debug = True
    manager.run()
