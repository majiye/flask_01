# -*- coding:utf-8 -*-
# 存放所有的后端接口 蓝图
from flask import Blueprint

api = Blueprint('api',__name__,url_prefix='/api/v1_0')

import index
import verify_code, passport, profile, house, order
# url_prefix='/api/v1_0'

# 增加请求钩子函数, 统一处理数据返回为JSON格式
@api.after_request
def after_request(response):

    # 为例避免个别接口的类型获取出现异常,需要做好判断
    # 默认: text/html text/plain
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response