# -*- coding:utf-8 -*-

# 公用的工具类
from werkzeug.routing import BaseConverter

# 创建路由转换器
class RegexConverter(BaseConverter):
    def __init__(self,url_map,regex):
        super(RegexConverter,self).__init__(url_map)
        self.regex = regex