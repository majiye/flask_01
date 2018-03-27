# -*- coding:utf-8 -*-

from flask import Flask

# 创建Flask类的实例， 即WIGS应用程序
app = Flask(__name__)


# 使用 route() 装饰器告诉 Flask 什么样的URL 能触发我们的函数
@app.route('/')
def index():
    return 'Hello World'

#lask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    # app.debug = True
    app.run(debug = True)