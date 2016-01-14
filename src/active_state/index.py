from flask import jsonify, request
import data.database.Mongo.test
from src import app
from src.common.veri import Ver
from src.model.person import Person
from util.macro import success_json

@app.route('/test', methods=['get'])
def test():
    # data1 = request.args.get('test', '123')
    bool_value = Ver.mail('82148941@qq.com')
    bool_value2 = Ver.ver_num('11111111')
    print(bool_value, bool_value2)
    return bool_value


@app.route("/test<int:number>/<string:name>")
def test2(number, name):
    print(number, name)
    data.database.Mongo.test.Tes(code='S').save()
    return 'ok'


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
        print(a.id)
    return 'ok'
