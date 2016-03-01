from functools import wraps

import jwt
import datetime
import time

from flask import request
from flask.ext.mongoengine import unicode

from data.database.Mongo.MongoUser import MongoUser, Token
from util.Encrypt import BcryptPassManager
from util.result_helper import result_success, result_fail


# （在登陆，注册，修改密码时）创建token 并保存token
def make_token(user_id):
    try:
        # 创建token
        token_value = BcryptPassManager.encrypt_pass(str(user_id))
        # 查找用户信息
        user = MongoUser.objects(mysql_id=user_id).first()
        # 保存token
        token = Token(value=token_value)
        MongoUser.objects(mysql_id=user_id).update(token=token)
        info = {
            'uid': user_id,
            'pic': user.info.pic,
            'nickname': user.info.nickname,
            'signature': user.info.signature,
            'sex': user.info.sex,
            'province': user.info.province,
            'city': user.info.city,
            'origin': user.info.user_origin,
            'hx_account': user.info.hx_account,
            'hx_password': user.info.hx_password,
            'is_verify': user.info.is_verify,
            'is_protect': user.info.is_protect
        }
        return result_success('成功', {'token': token_value, 'user_info': info})
    except Exception as e:
        print('创建保存token时出错', e)
        return result_fail('失败，创建token时出现异常')


# (api 请求 过滤token) 判断是否过期，无效
def filter_token(func):
    @wraps(func)
    def _filter_token():
        if request.method == 'GET':
            token = request.args.get('token')
        else:
            token = request.form.get('token')
        if token is None:
            return result_fail('token 参数是必须的')

        user = MongoUser.objects(token__value=token).first()
        if user is None:
            return result_fail('token 无效')
        else:
            if user.token.due_time < datetime.datetime.now():
                return result_fail('token 已经过期，请重新登陆获取token')

        data = {
            'id': user.mysql_id,
            'hx_account': user.info.hx_account,
            'nickname': user.info.nickname,
            'pic': user.info.pic
        }
        # data = TokenHelper.decrypt(token)
        # if data is None:
        #     return result_fail('token 无效或过期，请重新登陆')
        # else:
        #     if data['past_time'] < time.mktime(datetime.datetime.now()):
        #         return result_fail('token 无效或过期，请重新登陆')
        return func(data)

    return _filter_token


class TokenHelper(object):
    __key = 'benhu_xupei_888'

    def __init__(self, id, hx_account):
        self.__id = id
        self.__hx_account = hx_account

    def content(self):
        past_time = (datetime.datetime.now() + datetime.timedelta(seconds=24 * 60 * 60 * 60)).timetuple()
        content = {'id': self.__id, 'hx_account': self.__hx_account, 'past_time': time.mktime(past_time)}
        return content

    # 加密
    def encrypt(self):
        content = self.content()
        encoded = jwt.encode(content, TokenHelper.__key, algorithm='HS256')
        return unicode(encoded, 'utf-8')

    @staticmethod
    def decrypt(token):
        try:
            content = jwt.decode(token, TokenHelper.__key, algorithms=['HS256'])
            return content
        except Exception as e:
            print('token 解密失败 token无效', e)
            return None
