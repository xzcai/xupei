from src import app
from util.result_helper import result_fail
from util.token_helper import filter_token


def deco1(func):
    def _deco1():
        try:
            return func()
        except Exception as e:
            print('异常错误', str(e))
            return result_fail('异常错误' + str(e))

    return _deco1


@app.route("/con/test")
@deco1
def dd():
    print('123')
    return 'ok'


# @app.route("/con/test2")
# @deco1
# def dd2():
#     print('456')
#     return 'ok'

# @deco1
# def test00():
#     return 'ok'
#
#
#
# @app.route("/con/test")
# @deco1
# @filter_token
# def test11(token):
#     print('123546465')
#     a = 10 / 0
#     print(a)
#     return 'ok'
#
#
# @app.route('/ds/ss')
# @app.route('/ds/s')
# @deco1
# def test22():
#     return 'ok'

#
# @deco1
# @app.route("/con/test22", methods=['get'])
# def modify11():
#     print('dsf')
#     a = 10 / 0
#     print(a)
#     print('123456')
#     return 'ok'
