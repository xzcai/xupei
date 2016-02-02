import datetime

from bson import ObjectId
from flask import request
from mongoengine import Q
from data.database.Mongo.Activity import Activity, Address, ActivityCreator, ActivityTicket
from data.database.Mongo.MongoUser import MongoUser
from src import app
from src.bll.activity_bll import is_collection
from util.decorator_helper import filter_exception
from util.macro import Activity_Attribute
from util.result_helper import result_success, result_fail
from util.time_helper import time_to_stamp, stamp_to_time
from util.token_helper import filter_token


# 活动属性排序
def activity_sort(sort_attribute, where, page_index, page_size):
    if sort_attribute == Activity_Attribute.hot:
        objs = Activity.objects(where).order_by('-statistics.attend_count').exclude('tickets')
    if sort_attribute == Activity_Attribute.recommend:
        objs = Activity.objects(where).order_by('-statistics.recommend_count').exclude('tickets')
    elif sort_attribute == Activity_Attribute.free:
        where = where & Q(is_free=True)
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')
    elif sort_attribute == Activity_Attribute.near:
        objs = Activity.objects(where).order_by('-statistics.recommend_count').exclude('tickets')
    elif sort_attribute == Activity_Attribute.select:
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')
    else:
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')
    index = int(page_index) - 1
    size = int(page_size)
    return objs.skip(index * size).limit(size)


# 整合数据，去除无用数据
def activity_user_data(activity, user_id):
    item = {
        'id': activity.id,
        'poster': activity.poster,
        'queue_pics': activity.pics,
        'is_free': activity.is_free,
        'cast_much': activity.cast_much,
        'creator_info': activity.creator_info,
        'recommend_count': activity.statistics.recommend_count,
        'attend_count': activity.statistics.attend_count,
        'title': activity.title,
        'address': activity.address.address,
        'begin_time': time_to_stamp(activity.begin_time),
        'queue_begin_time': activity.queue_begin_time,
        'labels': activity.labels,
        'is_collection': is_collection(user_id, activity.id)
    }
    return item


# 首页 获取活动列表分页
@app.route("/activity/index", methods=['GET'])
@filter_exception
@filter_token
def get_index(token):
    creator_type = int(request.args.get("creator_type", 2))
    label = request.args.get('label')
    attribute = request.args.get("attribute", '')
    date = request.args.get('date', '')
    city_id = request.args.get("city_id")
    is_home = request.args.get("is_home", '')
    page_size = request.args.get("page_size", '')
    page_index = request.args.get("page_index", '')
    objs = Activity.objects(creator_info__creator_type=2, address__city_id=city_id,
                            end_time__gte=datetime.datetime.now()).order_by('-statistics.attend_count').order_by(
            '-statistics.recommend_count').exclude('tickets').skip(0).limit(30)
    data = []
    for o in objs:
        item = activity_user_data(o, token['id'])
        data.append(item)
    return result_success('获取数据成功', data)


@app.route("/activity/sponsor", methods=['GET'])
@filter_exception
@filter_token
def activity_sponsor(token):
    creator_type = int(request.args.get("creator_type", 2))
    label = request.args.get('label')
    attribute = request.args.get("attribute")
    date = request.args.get('date')
    city_id = request.args.get("city_id")
    is_home = request.args.get("is_home", '')
    page_size = request.args.get("page_size", '1')
    page_index = request.args.get("page_index", '50')

    where = Q(creator_info__creator_type=2) & Q(address__city_id=city_id)
    if label is not None:
        where = where & Q(labels=label)
    if date is not None:
        where = where & Q(begin_time__gte=stamp_to_time(date)) & Q(
                begin_time__lt=stamp_to_time(date) + datetime.timedelta(1))
    objs = activity_sort(attribute, where, page_size, page_index)
    data = []
    for o in objs:
        item = activity_user_data(o, token['id'])
        data.append(item)
    return result_success('获取数据成功', data)


@app.route("/activity/queue", methods=['GET'])
@filter_exception
@filter_token
def activity_queue(token):
    creator_type = int(request.args.get("creator_type", 2))
    label = request.args.get('label')
    attribute = request.args.get("attribute")
    date = request.args.get('date')
    city_id = request.args.get("city_id")
    is_home = request.args.get("is_home", '')
    page_size = request.args.get("page_size", '1')
    page_index = request.args.get("page_index", '50')

    where = Q(creator_info__creator_type=1) & Q(address__city_id=city_id)
    if label is not None:
        where = where & Q(labels=label)
    if date is not None:
        where = where & Q(begin_time__gte=stamp_to_time(date)) & Q(
                begin_time__lt=stamp_to_time(date) + datetime.timedelta(1))

    # objs = Activity.objects(creator_info__creator_type=2).order_by('create_time').exclude('tickets')
    objs = activity_sort(attribute, where, page_size, page_index)
    data = []
    for o in objs:
        item = {
            'poster': o.poster,
            'cast-much': o.cast_much,
            'creator_info': o.creator_info,
            'recommend_count': o.statistics.recommend_count,
            'attend_count': o.statistics.attend_count,
            'title': o.title,
            'address': o.address.address,
            'begin_time': time_to_stamp(o.begin_time),
            'labels': o.labels,
            'is_collection': is_collection(token['id'], o.id)
        }
        data.append(item)
    return result_success('获取数据成功', data)


# 获取活动详情
@app.route("/activity/detail", methods=['GET'])
def get_detail():
    pass


# 参加活动
@app.route("/activity/attend", methods=["GET", "POST"])
def attend():
    # aid = request.args.get("aid")
    pass


# 推荐活动
@app.route("/activity/recommend", methods=["GET", "POST"])
def recommend():
    pass


# 收藏活动
@app.route("/activity/collect", methods=["GET", "POST"])
@filter_exception
@filter_token
def activity_collect(token):
    aid = request.args.get("aid")

    # MongoUser.objects(__raw__={'mysql_id': token['id'], '$addToSet': {'activity_collect': aid}})
    MongoUser.objects(mysql_id=token['id']).update(add_to_set__activity_collect=[ObjectId('56b05c9e94a7c0ab54582b3d')])
    return result_success('sdf')


# 发布活动
@app.route("/activity/issue", methods=['get'])
def issue():
    ticket1 = ActivityTicket(name='贵宾票', inventory=20, description='5月20日 周杰伦盛大演出', price=1000, is_entity=True)
    ticket2 = ActivityTicket(name='普通票', inventory=20, description='5月20日 周杰伦盛大演出', price=200, is_entity=True)
    address = Address(longtitude='10.2', latitude='20.1', address='zhong yue', city_id=1)
    creator_info = ActivityCreator(name='咕噜米', pic='1.jpg', id=1, creator_type=2)
    d = Activity(title="qu da pai", address=address, poster='img/1.png', hx_group_id='123456789',
                 labels=['旅游', '沙发'], begin_time=datetime.datetime.now() + datetime.timedelta(seconds=3600 * 24 * 2),
                 end_time=datetime.datetime.now() + datetime.timedelta(
                         seconds=360000),
                 creator_info=creator_info, tickets=[ticket1, ticket2], is_free=True, cast_much='20').save()
    print(d.id)

    return 'ok'
