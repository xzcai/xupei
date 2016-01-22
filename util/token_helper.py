from functools import wraps

import jwt
import datetime
import time

from flask import request
from flask.ext.mongoengine import unicode

from data.database.Mongo.MongoUser import MongoUser, Token
from util.result_helper import result_success, result_fail


# （在登陆，注册，修改密码时）创建token 并保存token
def make_token(user_id):
    pass
    try:
        user = MongoUser.objects(mysql_id=user_id).first()
        token_helper = TokenHelper(user_id, user.info.hx_account)
        token_value = token_helper.encrypt()
        token = Token(value=token_value)
        MongoUser.objects(mysql_id=user_id).update(token=token)
        return result_success('成功', {'token': token_value, 'user_info': user.info})
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
            return result_fail('token 必填')
        data = TokenHelper.decrypt(token)
        if data is None:
            return result_fail('token 无效或过期，请重新登陆')
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
