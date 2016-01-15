import datetime

import data.database.Mongo.test
from data.model.person import Person
from src import app
from src.common.verify import Ver


@app.route("/time")
def timetest():
    print(datetime.datetime.utcnow())
    return  "ok"


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
def login():
    person = Person('cxz', 'gen', 12)
    print(person.address)
    print(person.get_test())
    print(Person.how_many())
    return person.get_test()[0]


@app.route("/user/find")
def find():
    data11 = data.database.Mongo.test.Tes.objects(code='S')
    for a in data11:
        print(a.id, a.code)
    return 'ok'
