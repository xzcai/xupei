import jwt
import datetime
from flask.ext.mongoengine import unicode
from data.database.Mongo.MongoUser import Token, MongoUser
from util.result_helper import result_success, result_fail


# （在登陆，注册，修改密码时）创建token 并保存token
def make_token(user_id, user_info):
    try:
        token_helper = TokenHelper(user_id, user_info.account, user_info.hx_account)
        token_value = token_helper.encrypt()
        token = Token(value=token_value)
        MongoUser.objects(mysql_id=user_id).update(token=token)
        return result_success('成功', {'token': token_value, 'user_info': user_info})
    except Exception as e:
        print('创建保存token时出错', e)
        return result_fail('失败，创建token时出现异常')


class TokenHelper(object):
    __key = 'benhu_xupei_888'

    def __init__(self, id, account, hx_account):
        self.__id = id
        self.__account = account
        self.__hx_account = hx_account

    def content(self):
        content = {'id': self.__id, 'account': self.__account, 'hx_account': self.__hx_account, 'login_time': str(datetime.datetime.now())}
        return content

    def encrypt(self):
        content = self.content()
        encoded = jwt.encode(content, TokenHelper.__key, algorithm='HS256')
        return unicode(encoded, 'utf-8')

    @staticmethod
    def decrypt(encoded):
        content = jwt.decode(encoded, TokenHelper.__key, algorithms=['HS256'])
        return content
