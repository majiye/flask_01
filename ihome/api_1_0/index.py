# -*- coding:utf-8 -*-
import logging
from . import api
from ihome import db
from flask import session
from ihome import models
# 使用 route() 装饰器告诉 Flask 什么样的URL 能触发我们的函数


@api.route('/')
def index():
    session['name'] = 'itcast'
    logging.fatal('111111') # 11111是日志信息
    logging.error('122222')
    logging.warn('warn')
    logging.info('info')
    logging.debug('debug')
    return 'Hello World'


@api.route('/demo',methods=['GET','POST'])
def demo():
    return 'demooo'