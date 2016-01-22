from _md5 import md5

import bcrypt

from flask.ext.mongoengine import unicode

import jwt


def EncryptPass(pwd):
    m2 = md5()
    m2.update(pwd.encode("utf8"))
    return m2.hexdigest()


class BcryptPassManager:
    @staticmethod
    def check_valid(password, hashed):
        # try:
            result = bcrypt.hashpw(password.encode("utf-8"), hashed.encode("utf-8"))
            if result == hashed.encode("utf-8"):
                return True
            else:
                return False
        # except Exception as e:
        #     print('校验密码时出现异常错误', e)
        #     return False

    @staticmethod
    def encrypt_pass(password):
        temp = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return unicode(temp, 'utf-8')

    @staticmethod
    def encrypt():  # content:明文
        encoded = jwt.encode({'some': 'payload', 'id': '1575704895111245452454', 'us': 'sdf'}, 'secret',
                             algorithm='HS256')
        print(encoded)
        return encoded

    @staticmethod
    def decrypt(encoded):  # content:密文
        d = jwt.decode(encoded, 'secret', algorithms=['HS256'])
        print(d)
        return d
