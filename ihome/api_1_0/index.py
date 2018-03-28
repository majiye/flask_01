# -*- coding:utf-8 -*-
from . import api

# 使用 route() 装饰器告诉 Flask 什么样的URL 能触发我们的函数
@api.route('/')
def index():
    return 'Hello World'