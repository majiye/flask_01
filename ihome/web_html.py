# -*- coding:utf-8 -*-
from flask import Blueprint,current_app,make_response
from flask_wtf.csrf import generate_csrf
# 创建静态文件的蓝图
html = Blueprint('html',__name__)


# 用一个路由来匹配所有的url
@html.route('/<re(r".*"):file_name>')
def web_html(file_name):
    # 1 没有文件名  自行拼接首页
    if not file_name:
        file_name = 'index.html'
    # 2 文件名不是favicon.ico 再拼接html/路径
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name
    print file_name

    # return current_app.send_static_file(file_name)

    # 创建response
    response = make_response(current_app.send_static_file(file_name))
    ## 这里还需要设置csrf_token
    csrf_token = generate_csrf()

    # 设置cookie
    response.set_cookie('csrf_token', csrf_token)
    # Flask-WTF的generate_csrf, 会将cookie中的csrf_token信息, 会同步到session中
    # Flask-Session又会讲session中的csrf_token, 同步到redis中
    # generate_csrf不会每次调用都生成. 会先判断浏览器的cookie中的session里是否有csrf_token信息.没有才重新生成
    # 常规的CSRF保护机制, 是从浏览器的cookie中获取. 而Flask-WTF的扩展机制不一样, 是从session信息中获取csrf_token保护机制

    return response