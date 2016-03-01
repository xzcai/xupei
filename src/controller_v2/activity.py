import datetime

from bson import ObjectId
from flask import request
from mongoengine import Q
from data.database.Mongo.Activity import Activity, Address, ActivityCreator, ActivityTicket
from data.database.Mongo.MongoUser import MongoUser, ActivityState
from src import app
from src.bll.activity_bll import is_collection
from util.calculate_distance import calc_distance
from util.decorator_helper import filter_exception
from util.image_helper import ImageHelper, PicType
from util.macro import Activity_Attribute
from util.request_helper import request_all_values
from util.result_helper import result_success, result_fail
from util.time_helper import time_to_stamp, stamp_to_time, time_array_to_stamp
from util.token_helper import filter_token


# 活动属性排序
def activity_sort(sort_attribute, where, page_index, page_size, longitude=None, latitude=None):
    if sort_attribute == Activity_Attribute.hot:
        objs = Activity.objects(where).order_by('-statistics.attend_count').exclude('tickets')
    elif sort_attribute == Activity_Attribute.recommend:
        objs = Activity.objects(where).order_by('-statistics.recommend_count').exclude('tickets')
    elif sort_attribute == Activity_Attribute.free:
        where = where & Q(is_free=True)
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')
    elif sort_attribute == Activity_Attribute.near:
        print(longitude, latitude)
        objs = Activity.objects(where).exclude('tickets')
        data = []
        for o in objs:
            o.distance = calc_distance(float(latitude), float(longitude), float(o.address.latitude),
                                       float(o.address.longtitude))
            data.append(o)
        print(data)
        return sorted(data, key=lambda x: x['distance'])

    elif sort_attribute == Activity_Attribute.select:
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')
    else:
        objs = Activity.objects(where).order_by('create_time').exclude('tickets')

    size = int(page_size)
    num = (int(page_index) - 1) * size
    return objs
    return objs.skip(num).limit(size)


# 整合数据，去除无用数据
def activity_user_data(activity, user_id):
    if activity.creator_info.creator_type == 1:
        item = {
            'aid': str(activity.id),
            'pics': activity.pics,
            'creator_name': activity.creator_info.name,
            'creator_pic': activity.creator_info.pic,
            'recommend_count': activity.statistics.recommend_count,
            'attend_count': activity.statistics.attend_count,
            'title': activity.title,
            'address': activity.address.address,
            'labels': activity.labels,
            'is_collection': is_collection(user_id, activity.id),
            'is_free': activity.is_free,
            'begin_time': time_array_to_stamp(activity.queue_begin_time)
        }
    else:
        item = {
            'aid': str(activity.id),
            'poster': activity.poster,
            'cast_much': activity.cast_much,
            'creator_name': activity.creator_info.name,
            'creator_pic': activity.creator_info.pic,
            'recommend_count': activity.statistics.recommend_count,
            'attend_count': activity.statistics.attend_count,
            'title': activity.title,
            'address': activity.address.address,
            'begin_time': time_to_stamp(activity.begin_time),
            'labels': activity.labels,
            'is_collection': is_collection(user_id, activity.id),
        }
    return item


@app.route("/activity/sponsor", methods=['GET'])
@filter_exception
@filter_token
def activity_sponsor(token):
    label = request.args.get('label')
    attribute = request.args.get("attribute")
    date = request.args.get('date')
    city_id = request.args.get("city_id")
    page_size = request.args.get("page_size", '1')
    page_index = request.args.get("page_index", '30')
    longitude = request.args.get("longitude", '')
    latitude = request.args.get("latitude", '')
    where = Q(creator_info__creator_type=2) & Q(address__city_id=city_id) & Q(end_time__gt=datetime.datetime.now())
    if label:
        where = where & Q(labels=label)
    if date:
        where = where & Q(begin_time__gte=stamp_to_time(date)) & Q(
                begin_time__lt=stamp_to_time(date) + datetime.timedelta(1))
    if attribute is not None:
        objs = activity_sort(attribute, where, page_index, page_size, longitude, latitude)
    # 首页
    else:
        objs = Activity.objects(where).order_by('-statistics.attend_count').order_by(
                '-statistics.recommend_count').exclude('tickets').skip(0).limit(30)
    data = []
    for o in objs:
        item = activity_user_data(o, token['id'])
        data.append(item)
    return result_success('获取数据成功', data)


@app.route("/activity/queue", methods=['GET'])
@filter_exception
@filter_token
def activity_queue(token):
    label, attribute, date, city_id, page_size, page_index, longitude, latitude = request_all_values('label',
                                                                                                     'attribute',
                                                                                                     'date',
                                                                                                     'city_id',
                                                                                                     'page_size',
                                                                                                     'page_index',
                                                                                                     'longitude',
                                                                                                     'latitude')
    if page_size is None:
        page_size = 30
    if page_index is None:
        page_index = 1

    where = Q(creator_info__creator_type=1) & Q(address__city_id=city_id) & Q(
            queue_begin_time__gt=datetime.datetime.now())
    if label:
        where = where & Q(labels=label)
    if date:
        begin_time = stamp_to_time(date)
        where = where & Q(queue_begin_time__gte=begin_time) & Q(
                queue_begin_time__lt=begin_time + datetime.timedelta(1))

    objs = activity_sort(attribute, where, page_size, page_index, longitude, latitude)
    data = []
    for o in objs:
        item = activity_user_data(o, token['id'])
        data.append(item)
    return result_success('获取数据成功', data)


# 获取活动详情
@app.route("/activity/detail", methods=['GET'])
@filter_exception
@filter_token
def get_detail(token):
    id = request_all_values('id')
    activity = Activity.objects(id=id).first()
    data = {
        'id': id,
        'hx_qid': activity.hx_group_id,
        'creator_info': activity.creator_info,
        'labels': activity.labels,
        'attend_count': activity.statistics.attend_count,
        'recommend_count': activity.statistics.recommend_count
    }
    return result_success('成功', data)


# 参加活动
@app.route("/activity/attend", methods=["GET", "POST"])
@filter_exception
@filter_token
def attend(token):
    is_city, is_friend, content, aid, pics = request_all_values('is_city', 'is_friend', 'content', 'aid', 'pics')
    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.dynamic)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)

    if is_friend == 'true':
        is_friend = True
    if is_city == 'true':
        is_city = True

    obj = MongoUser.objects(mysql_id=token['id'], activity_state__activity=ObjectId(aid),
                            activity_state__active_type=2).first()
    if obj is not None:
        return result_fail('已经参加过该活动')
    # 构建推荐对像
    activity = Activity(id=aid)
    activity_state = ActivityState(active_type=2, object_id=ObjectId(), content=content, pics=pic_array,
                                   activity=activity, is_city=is_city, is_friend=is_friend)
    # 推荐到活动态
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)
    # 添加活动添加数
    Activity.objects(id=aid).update(inc__statistics__attend_count=1)
    return result_success('推荐活动成功')


# 推荐活动
@app.route("/activity/recommend", methods=["GET", "POST"])
@filter_exception
@filter_token
def recommend(token):
    is_city, is_friend, content, aid, pics = request_all_values('is_city', 'is_friend', 'content', 'aid', 'pics')
    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.dynamic)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)

    if is_friend == 'true':
        is_friend = True
    if is_city == 'true':
        is_city = True

    obj = MongoUser.objects(mysql_id=token['id'], activity_state__activity=ObjectId(aid),
                            activity_state__active_type=1).first()
    if obj is not None:
        return result_fail('已经推荐过该活动')
    # 构建推荐对像
    activity = Activity(id=aid)
    activity_state = ActivityState(active_type=1, object_id=ObjectId(), content=content, pics=pic_array,
                                   activity=activity, is_city=is_city, is_friend=is_friend)
    # 推荐到活动态
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)
    # 添加活动添加数
    Activity.objects(id=aid).update(inc__statistics__recommend_count=1)
    return result_success('推荐活动成功')


# 收藏活动(收藏和取消收藏)
@app.route("/activity/collect", methods=["GET", "PUT"])
@filter_exception
@filter_token
def activity_collect(token):
    if request.method == 'GET':
        aid = request.args.get("aid")
    else:
        aid = request.form.get("aid")
    obj = MongoUser.objects(mysql_id=token['id'], activity_collect=ObjectId(aid)).first()
    if obj is None:
        MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_collect=ObjectId(aid))
        Activity.objects(id=aid).update(inc__statistics__collect_count=1)
        return result_success('收藏成功')
    else:
        MongoUser.objects(mysql_id=token['id']).update_one(pull__activity_collect=ObjectId(aid))
        Activity.objects(id=aid).update(dec__statistics__collect_count=1)
        return result_success('取消收藏成功')


# 发布活动
@app.route("/activity/issue", methods=['get'])
def issue():
    type = request.args.get("type")

    address = Address(longtitude='120.208261', latitude='30.247119', address='zhong yue', city_id=1)
    ticket1 = ActivityTicket(name='贵宾票', inventory=20, description='5月20日 周杰伦盛大演出', price=1000, is_entity=True)
    ticket2 = ActivityTicket(name='普通票', inventory=20, description='5月20日 周杰伦盛大演出', price=200, is_entity=True)
    if type is None:
        creator_info = ActivityCreator(name='咕噜米', pic='1.jpg', id=1, creator_type=2)
        Activity(title="z这是  03-05 的 活动", address=address, poster='img/1.png', hx_group_id='123456789',
                 labels=['旅游', '沙发'],
                 begin_time=datetime.datetime.now() + datetime.timedelta(4),
                 end_time=datetime.datetime.now() + datetime.timedelta(5),
                 creator_info=creator_info, tickets=[ticket1, ticket2], is_free=True, cast_much='20').save()
    else:
        creator_info = ActivityCreator(name='咕噜米', pic='1.jpg', id=2, creator_type=1)
        Activity(title="这是  03-09 的 活动", address=address, pics=['1.jpg'], hx_group_id='123456789',
                 labels=['旅游', '沙发'], creator_info=creator_info, is_free=True,
                 queue_begin_time=[datetime.datetime.now() + datetime.timedelta(8)]).save()
    return 'ok'


# 获取标签及标签活动
@app.route("/activity/label", methods=['get'])
@filter_exception
@filter_token
def activity_label(token):
    page_index = request_all_values('page_index')
    data = [{'label': '户外', 'num': 1}, {'label': '旅游', 'num': 1}, {'label': '聚会', 'num': 1}, {'label': '展览', 'num': 1},
            {'label': '骑行', 'num': 1}, {'label': '艺术', 'num': 1}]
    return result_success('成功', data)
