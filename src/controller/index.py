import datetime
import requests
from flask import json

import data.database.Mongo.test
from data.database.Mongo.HxToken import HxToken
from data.model.person import Person
from src import app
from util.hx import HxHelper
from util.phone_helper import PhoneHelper
from util.result_helper import result_success
from util.verify import Ver


@app.route("/time")
def timetest():
    print(datetime.datetime.utcnow())
    return "ok"


@app.route('/test', methods=['get'])
def test():
    # data1 = request.args.get('test', '123')
    # bool_value = Ver.mail('82148941@qq.com')
    # bool_value2 = Ver.ver_num('11111111')

    result = Ver(email="121321@asdf.com").begin_check()

    print(result)
    return '11111111'


@app.route("/test<int:number>/<string:name>")
def test2(number, name):
    print(number, name)
    data.database.Mongo.test.Tes(code='S').save()
    return 'ok111'


@app.route("/user/login", methods=['get'])
def index_login():
    person = Person('cxz', 'gen', 12)
    print(person.address)
    print(person.get_test())
    print(Person.how_many())
    return person.get_test()[0]


@app.route("/test1")
def test1():
    HxHelper.create_account('sdfss', 'sdssf', 'dsf')
    return 'ok'


@app.route("/user/find")
def find():
    data11 = data.database.Mongo.test.Tes.objects(code='S')
    for a in data11:
        print(a.id, a.code)
    return 'ok'


@app.route("/mongo")
def mongotest():
    # HxToken(value='123', past_due=datetime.datetime.utcnow).save()

    timespan = datetime.datetime.now() + datetime.timedelta(seconds=120)
    print(timespan)
    # for a in fate:
    #     print(a.id,'sdfs')
    return 'sdf'


@app.route("/register")
def test_register():
    print('jinlai')
    jsons = {'account': '123', 'password': '1234565', 'pic': '1.jpg', 'nickname': 'cxz', 'sex': 1, 'province': 'jiangx',
             'city': 'lep'}
    try:
        re = requests.post("localhost:8878/user/register", json.dumps(jsons))
        print(re)
    except Exception as e:
        print(e)
    return 'ok'


@app.route('/send')
def send():
    data = [{'d': 's'}]
    return result_success('chengg')
