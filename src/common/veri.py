import re


class Ver(object):
    # 静态方法
    @classmethod
    def phone(cls, phone_number):
        pass

    @classmethod
    def mail(cls, inputmail):
        ver_reslt = bool(
                re.match(r"^[a-zA-Z](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$",
                         inputmail, re.VERBOSE))

        print(ver_reslt)
        return 'ok'

    @classmethod
    def ver_num(cls, inputmail):
        ver_reslt = bool(
                re.match(r"[a-zA-Z0-9]{8}",
                         inputmail, re.VERBOSE))

        print(ver_reslt)
        return 'ok'
