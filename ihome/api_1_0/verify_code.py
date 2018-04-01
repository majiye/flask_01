# -*- coding:utf-8 -*-
import logging
import random

from flask import make_response, jsonify
from flask import request

from ihome import redis_store
from ihome.api_1_0 import api
from ihome.libs.yuntongxun.sms import CCP
from ihome.models import User
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
# from . import api
# 获取图片验证码
# 请求方式GET
# 路由： image_codes
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    # 1 实用工具类生成验证码
    name, text, image_data = captcha.generate_captcha()
    #将验证码的数据和编号存储到 redis 中
    # 对数据库操作要try一下 避免存取出错
    try:
        #redis_store.set() 设置数据
        #redis_store.expires()设置有效期
        #setex：设置数据的同时设置有效期
        # 第一位key 第二位：有效期 第三位：value
        redis_store.setex('image_code_%s' % image_code_id, 300,text)
    except Exception as e:
        # 记录日志
        logging.error(e)
        resp = {
            'error':RET.DBERR,
            'errmsg':'redis保存出错'
        }
    # 返回图像
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp

    # 获取短信验证码
    # 请求方法get
    # 路由：sms_codes
    # 参数：手机号 / 图像验证码 / 编号
    @api.route('/sms_codes/<re(r"1[3456789][0-9]{9}"):mobile>')
    def get_sms_codes(mobile):
        # 一 获取参数 ： 图像验证码 / 图像编码
        image_code = request.args.get('image_cade')
        image_code_id  = request.args.get('image_code_id')

        # 二 校验参数 ：判断完整性
        # 如果数据不为空 继续向下执行
        if not all([image_code,image_code_id]):
            resp = {
                'errno':RET.PARAMERR,
                'errmsg':'参数不全'
            }
            return jsonify(resp)
        # 三 逻辑处理
        # 1 从redis中获取数据对比
        # 2 判断用户是否已经注册
        # 3 调用第三方SDK发短信

        # 1-1 从redis获取验证码（键值）
        try:
            real_image_code = redis_store.get('image_code_%s' % image_code_id)
        except Exception as e:
            logging.error(e)
            resp = {
                'errno':RET.DBERR,
                'errmsg':'redis读取数据失败'
            }
            return jsonify(resp)
        # 1-2首先判断数据是否为none
        if real_image_code is None:
            resp = {
                'errno':RET.DATAERR,
                'errmsg':'验证码已过期，请重新刷新获取'
            }
            return jsonify(resp)
        # 1-3无论是否对比成功 都要先删除数据库的验证码 确保验证码只能验证一次
        try:
            redis_store.delete('image_code_%s' % image_code_id)
        except Exception as e:
            logging.error(e)
            resp = {
                'errno':RET.DBERR,
                'errmsg':'redis删除失败'
            }
            return jsonify(resp)
        # 1-4 与从请求端发来验证码进行对比
        if real_image_code.lower() != image_code.lower():
            resp = {
                'errno':RET.DATAERR,
                'errmsg':'验证码填写错误，请刷新后重试'
            }
            return jsonify(resp)

        # 2 判断用户是否注册过
        # 2-1 查询数据库的操作
        # 2-2 判断数据是否为None
        try:
            # 属性：mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
            user = User.query.filter_by(mobile=mobile).first()
        except Exception as e:
            logging.error(e)
            resp = {
                'errno':RET.DBERR,
                'errmsg':'mysql查询失败'
            }
            return jsonify(resp)
        else:
            # 执行成功走else
            if user is not None:
                # 用户已经注册过
                resp = {
                    'errno':RET.DATAERR,
                    'errmsg':'该用户的手机已经注册'
                }
                return jsonify(resp)

        # 3 调用第三方SDF发短信
        # 3—1 创建6位短信验证码 000000
        # import random
        sms_code = '%06d' % random.randint(0,999999)

        # 3_2 保存到redis中
        try:
            redis_store.setex('sms_code_%s' % mobile, 300, sms_code)
        except Exception as e:
            logging.error(e)
            resp = {
                'errno':RET.DBERR,
                'errmsg':'redis保存失败'
            }
            return jsonify(resp)
        # 3-3 发送验证码
        ccp = CCP()
        result = ccp.send_template_sms(mobile,[sms_code,'5'],1)

        # 四 返回数据
        if result == '000000':
            resp = {
                'errno':RET.OK,
                'errmsg':'发送短信成功'
            }
            return jsonify(resp)
        else:
            resp = {
                'errno':RET.THIRDERR,
                'errmsg':'发送短信失败'
            }
            return jsonify(resp)
