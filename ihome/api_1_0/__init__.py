# -*- coding:utf-8 -*-
# 存放所有的后端接口 蓝图
from flask import Blueprint

api = Blueprint('api',__name__,url_prefix='/api/v1_0')

import index