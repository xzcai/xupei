import datetime
import requests
from flask import json

import data.database.Mongo.test
from data.database.Mongo.HxToken import HxToken
from data.model.person import Person
from src import app
from util.Encrypt import EncryptPass, BcryptPassManager
from util.hx import HxHelper
from util.image_helper import ImageHelper, PicType
from util.phone_helper import PhoneHelper
from util.result_helper import result_success, result_fail
from util.token_helper import make_token, TokenHelper
from util.verify import Ver


def print1(func):
    print('123456')
    def print_j():
        print1('123213')
        func()
        print1('123213')
        return 'sdfs'
    return print_j






@app.route("/time")
@print1
def timetest():
    print('000000')
    return 'ok'


@app.route('/test', methods=['get'])
def test():
    # data1 = request.args.get('test', '123')
    # bool_value = Ver.mail('82148941@qq.com')
    # bool_value2 = Ver.ver_num('11111111')

    result = Ver(email="121321@asdf.com").begin_check()

    print(result)
    return '11111111'


@app.route("/test1")
def test1():
    leniystr = "VBORw0KGgoAAAANSUhEUgAAACwAAAAOCAYAAABU4P48AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAF6SURBVEhL1ZY9coMwEIWfchZIkckJxAmAhoojiNJu3KV0lwZK+xRU6ATmBJkUEXdRVj8MmGFsk9ge+5vReFlb2of0diymCTwRL0CHKmJgjKGQPnszJAqqw1iEqvOphZDgexJjRweq9QGrwKcWcmfB/+cCwf0xDiMan2dXIZp870ZBM6ecsIQs7Lzx2rLwa428ekawKZBgTxEvFbQqwSlu1+G830VDx61Qmh/RrO0So8YZBH2060//ohK1KUyILHYBcVqwrK1YgxHJwjVa//z1MxUj0OzMwgFe311mGTEyo5gq1kZxX5uX2Ax6L/QwTVK2WYZxmHYNf0Pow78SO8XYk2Lpt5fnKW3BwGWC228oH8756mrEG2enfYLEbS/y9HhjTgvuF6DDSaIKHTXYdsZX1yNAmtuCDp5jovfcDgdYHTQa1w0IrYc5SqVh7XoDgjS3jW0QH6sjO1jMX/NDoUpNgum6IHTjU2MeSLDSZD9zr7FDzKklnuzyA/wCcpDKoLig94YAAAAASUVORK5CYII="
    if ImageHelper.base64_to_image(leniystr, PicType.user) is None:
        return result_fail('图片上传出错')
    return result_success('成功')


def func():

    num = 10 / 0
    print(num)



@app.route("/test2")
def test2():
    token = BcryptPassManager.encrypt()
    content = BcryptPassManager.decrypt(token)

    print('12332456789',make_token(1,3,4))
    print(TokenHelper.decrypt(make_token(1,3,4)))

    print(content['id'])
    return 'ok'
