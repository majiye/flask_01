# -*- coding: utf-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config

"""
工具类与SDK的区别

工具类: 没有商业利益, 拿来直接使用的.

SDK: 开发组件包,保护代码/文档/示例....
    1. 官网, 是有商业价值利益的. 通常由某个公司来维护开发该产品
    2. 都需要注册/登录/创建应用(有控制台)/
    3. 获取AK、SK等才能使用. 都需要鉴权后才能使用
    4. 详细的接口文档/Demo/技术支持等
"""

# 需要填写你的 Access Key 和 Secret Key
access_key = 'ATldzdlglgNtZr-Ju5QtGHW4punC3D3GHppZSjeI'
secret_key = 'Y1r_uIDpfMPFoLbcLR_SCbbyna5PEnoCb72SYbK3'

# 我们使用此工具类的目的, 是调用存储图像方法后, 能够获得图像名-->给用户的用户头像路径赋值
def storage(file_data):
    """上传图片到七牛, file_data是文件的二进制数据"""
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'eeeee'

    # 我们不需要这个Key. 七牛会自动生成 所以定义为None
    # 上传到七牛后保存的文件名
    # key = 'my-python-logo.png';
    # 这里把key 设为None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    # 我们这个是通过form表单提交的, 不需要用到put_file方法
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, None, file_data)

    ret, info = put_data(token, None, file_data)

    print 'info: %s' % info
    print 'ret: %s' % ret

    if info.status_code == 200:
        # 表示上传成功， 返回文件名
        # 我们上传成功之后, 需要在别的页面显示图像, 因此需要返回图像名
        return ret.get("key")
    else:
        # 表示上传失败
        raise Exception("上传失败")
        # http://ozcxm6oo6.bkt.clouddn.com/FnTUusE1lgSJoCccE2PtYIt0f7i3


if __name__ == '__main__':
    # 打开图片数据
    # rb: 以二进制读
    with open("./003.jpg", "rb") as f:
        # 读取图片数据二进制数据
        file_data = f.read()
        # 上传图片书记到七牛云
        result = storage(file_data)
        # result 就存储的是图片名. 将来就可以再程序中调用显示
        print result
