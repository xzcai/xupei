from _md5 import md5

import bcrypt as bcrypt


def EncryptPass(pwd):
    m2 = md5()
    m2.update(pwd.encode("utf8"))
    return m2.hexdigest()


class BcryptPassManager:
    @staticmethod
    def check_valid(password, hashed):
        result = bcrypt.hashpw(password.encode("utf-8"), hashed.encode("utf-8"))
        if result == hashed.encode("utf-8"):
            return True
        else:
            return False

    @staticmethod
    def encrypt_pass(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
