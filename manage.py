# -*- coding:utf-8 -*-
'''主要负责程序的启动 以及 数据库的操作'''
from flask_script import Manager  # 启动扩展包
from flask_migrate import Migrate, MigrateCommand  # 迁移命令扩展包
from config import ProductionConfig,DevelopmentConfig
from ihome import create_appdb
# 函数create_appdb的参数 可以控制项目是调试模式 还是发布模式
app,db = create_appdb(DevelopmentConfig) # 发布模式

manager = Manager(app)
# 迁移操作 第一个参数是flask实例 第二个参数是SQLALchemy实例
migrate = Migrate(app, db)
# 对数据库增加可迁移操作命令
manager.add_command('db', MigrateCommand)


# 使用 route() 装饰器告诉 Flask 什么样的URL 能触发我们的函数
@app.route('/')
def index():
    return 'Hello World'


# lask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    # app.debug = True
    manager.run()
