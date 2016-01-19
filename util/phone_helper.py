import requests


class PhoneHelper:
    __str_reg = '101100-WEB-HUAX-458221'
    __str_pwd = 'AAAAAAAA'
    __url = 'http://www.stongnet.com/sdkhttp/sendsms.aspx'
    __source_add = ''
    __header = {'content-type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}

    @staticmethod
    def send(phone, code):
        str_content = '您的验证码为：' + str(code) + ' 【笨虎科技】'
        str_send = 'reg=' + PhoneHelper.__str_reg + '&pwd=' + PhoneHelper.__str_pwd + '&phone=' + phone + '&content=' + str_content + '&sourceadd=' + PhoneHelper.__source_add
        result = requests.post(PhoneHelper.__url, str_send.encode('utf-8'), headers=PhoneHelper.__header)
        if result.status_code == requests.codes.ok:
            return True
        else:
            return False
