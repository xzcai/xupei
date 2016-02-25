# 活动态  动态
from data.database.Mongo.MongoUser import MongoUser
from src import app
from util.decorator_helper import filter_exception
from util.result_helper import result_success
from util.token_helper import filter_token


# 获取活动态数据分页(查看自己和好友的)
@app.route("/dynamic/myself", methods=['GET'])
@filter_exception
@filter_token
def myself(token):
    uid = token['id']
    obj = list(MongoUser.objects(mysql_id=uid).only('friends').first().friends)
    obj.append(uid)

    active_state = []
    obj = MongoUser.objects(mysql_id__in=obj).order_by('-activity_state__add_time').only('activity_state')
    for data in obj:
        for d in range(0, len(data.activity_state)):
            active_state.append(data.activity_state[d])

    result = sorted(active_state, key=lambda x: x['add_time'], reverse=True)
    return result_success('获取数据成功', result)


# 获取活动态最新动态数
@app.route("/dynamic/new/num", methods=['GET'])
@filter_exception
@filter_token
def get_new_num(token):
    # user = MongoUser.objects(mysql_id__in=token['id']).only('activity_num').first()
    return result_success('成功', 2)


# 获取活动态最新动态信息
@app.route("/dynamic/new/info", methods=['GET'])
@filter_exception
@filter_token
def get_new_info(token):
    data = [{'id': 1, 'pic': '1.jpg', 'name': 'xzca', 'add_time': 1456297486, 'type': 1},
            {'id': 2, 'pic': '2.jpg', 'name': 'xzddca', 'add_time': 1456297306, 'type': 1}]
    return result_success('成功', data)
