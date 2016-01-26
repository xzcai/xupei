import re


class Ver:
    def __init__(self, phone=None, email=None, password=None):
        self.__email = '^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$'
        self.__phone = '^(((13[0-9]{1})|(15[0-9]{1})|(17[0-9]{1})|(18[0-9]{1})|(147))+\d{8})$'
        # 只能以字母开头（包括数字 字母 下划线【6-16】）
        self.__passwod = '^[a-zA-Z]\w{5,17}$'
        self.phone = phone
        self.email = email
        self.password = password
        self.succeed = True

    # 验证封装
    def verify(f):
        def verify(str_check, regular_expression):
            res = True
            print('in:' + str_check + regular_expression)
            ver_reslt = bool(
                    re.match(r"" + str(regular_expression) + "",
                             str_check, re.VERBOSE))
            if ver_reslt:
                res = True
            else:
                res = False
            if res:
                return f(str_check, regular_expression)
            return res

        return verify

    def begin_check(self):
        if self.phone:
            self.succeed = self.check(self.phone, self.__phone)
        if self.succeed and self.email:
            self.succeed = self.check(self.email, self.__email)
        return self.succeed

    @staticmethod
    @verify
    def check(str, expression):
        return False

        # @verify
        # def _test_email(self):
        #     return True
        #
        #
        #     # # 静态方法
        #     # @classmethod
        #     # def phone(cls, phone_number):
        #     #     pass
        #     #
        #     # @classmethod
        #     # def mail(cls, inputmail):
        #     #     ver_reslt = bool(
        #     #             re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
        #     #                      inputmail, re.VERBOSE))
        #     #
        #     #     print(ver_reslt)
        #     #     return 'ok'
        #     #
        #     # @classmethod
        #     # def ver_num(cls, inputmail):
        #     #     ver_reslt = bool(
        #     #             re.match(r"[a-zA-Z0-9]{8}",
        #     #                      inputmail, re.VERBOSE))
        #     #
        #     #     print(ver_reslt)
        #     #     return 'ok'
