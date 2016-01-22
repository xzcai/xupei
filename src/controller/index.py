import requests
from flask import json, request

import data.database.Mongo.test
from data.database.Mongo.HxToken import HxToken
from data.model.person import Person
from src import app
from util.Encrypt import EncryptPass, BcryptPassManager
from util.hx import HxHelper
from util.image_helper import ImageHelper, PicType
from util.phone_helper import PhoneHelper
from util.result_helper import result_success, result_fail
from util.token_helper import TokenHelper
from util.verify import Ver
import datetime
import time








def deco(func):
    def _deco():
        if request.method == 'POST':
            token = request.form.get('token')
        else:
            token = request.args.get('token')
        print(token)
        print("before myfunc() called")
        func()

    return _deco


@app.route("/time")
@deco
def timetest():
    print('sdfs')
    data = TokenHelper.decrypt(
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjE5LCJhY2NvdW50IjoiMTU3NTcwNDg5NjEiLCJoeF9hY2NvdW50IjoiMTU3NTcwNDg5NjEifQ.iPgNKTIszyV3ipRuqlZWPLiDdMSf5S4IfXOMpvs20')
    print(data)

    tt = str(datetime.datetime.now() + datetime.timedelta(seconds=-24 * 60 * 60 * 60))
    print(tt)

    ttt = (datetime.datetime.now() + datetime.timedelta(seconds=24 * 60 * 60 * 60)).timetuple()
    print(time.mktime(ttt))

    timestamp = time.mktime(datetime.datetime.now().timetuple())
    print(timestamp)
    ltime = time.localtime(timestamp)
    print(ltime)

    tttt = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    print(tttt)
    if tt > str(datetime.datetime.now()):
        print('yes')
    else:
        print('no')

    return '1111111'


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
    print(BcryptPassManager.encrypt_pass('456321'))
    return 'ok'
