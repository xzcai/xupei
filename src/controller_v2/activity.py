import datetime
import json
import random

from bson import ObjectId
from flask import request
from mongoengine import Q
from data.database.Mongo.Activity import Activity, Address, ActivityCreator, ActivityTicket, TicketInfo
from data.database.Mongo.MongoUser import MongoUser, ActivityState
from src import app
from src.bll.activity_bll import is_collection
from src.helper.activity import time_transform
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
    size = int(page_size)
    start = (int(page_index) - 1) * size
    print(size, start, page_index, page_size)

    if sort_attribute == Activity_Attribute.hot:
        objs = Activity.objects(where).order_by('-statistics.attend_count')[start:start + size]
    elif sort_attribute == Activity_Attribute.recommend:
        objs = Activity.objects(where).order_by('-statistics.recommend_count')[start:start + size]
    elif sort_attribute == Activity_Attribute.free:
        where = where & Q(is_free=True)
        objs = Activity.objects(where).order_by('create_time')[start:start + size]
    elif sort_attribute == Activity_Attribute.near:
        print(longitude, latitude)
        objs = Activity.objects(where)[start:start + size]
        data = []
        for o in objs:
            o.distance = calc_distance(float(latitude), float(longitude), float(o.address.latitude),
                                       float(o.address.longtitude))
            data.append(o)
        print(data)
        return sorted(data, key=lambda x: x['distance'])

    elif sort_attribute == Activity_Attribute.select:
        objs = Activity.objects(where).order_by('create_time')[start:start + size]
    else:
        objs = Activity.objects(where).order_by('create_time').skip(start).limit(size)

    return objs


# 整合数据，去除无用数据
def activity_user_data(activity, user_id):
    if activity.creator_info.creator_type == 1:
        item = {
            'aid': str(activity.id),
            'pics': activity.pics,
            'creator_name': activity.creator_info.name,
            'creator_pic': activity.creator_info.pic,
            'creator_id': activity.creator_info.id,
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
            'creator_id': activity.creator_info.id,
            'recommend_count': activity.statistics.recommend_count,
            'attend_count': activity.statistics.attend_count,
            'title': activity.title,
            'address': activity.address.address,
            'time': time_transform(activity.begin_time, activity.end_time),
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
        where = where & Q(begin_time__lte=stamp_to_time(date, True)) & Q(end_time__gte=stamp_to_time(date, True))
    if attribute is not None:
        objs = activity_sort(attribute, where, page_index, page_size, longitude, latitude)
    # 首页
    else:
        objs = Activity.objects(where).order_by('-statistics.attend_count').order_by(
                '-statistics.recommend_count').skip(0).limit(30)
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
        where = where & Q(queue_begin_time__gte=begin_time) & Q(queue_begin_time__lt=begin_time + datetime.timedelta(1))

    objs = activity_sort(attribute, where, page_index, page_size, longitude, latitude)
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
    aid = request_all_values('aid')

    obj = MongoUser.objects(mysql_id=token['id'], activity_attend=ObjectId(aid)).first()
    if obj is not None:
        return result_fail('已经参加过该活动')

    # 添加活动添加数
    Activity.objects(id=aid).update(inc__statistics__attend_count=1)
    # 添加用户参加活动
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_attend=ObjectId(aid))
    return result_success('参加活动成功')


# 参加活动 添加到活动态
@app.route("/activity/attend/dynamic", methods=["GET", "POST"])
@filter_exception
@filter_token
def attend_dynamic(token):
    city_id, is_friend, content, aid, pics = request_all_values('city_id', 'is_friend', 'content', 'aid', 'pics')
    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.dynamic)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)

    if is_friend == 'true':
        is_friend = True
    # 构建推荐对像
    activity = Activity(id=aid)
    activity_state = ActivityState(active_type=2, object_id=ObjectId(), content=content, pics=pic_array,
                                   activity=activity, city_id=int(city_id), is_friend=is_friend)
    # 推荐到活动态
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)
    return result_success('参加活动成功')


# 推荐活动
@app.route("/activity/recommend", methods=["GET", "POST"])
@filter_exception
@filter_token
def recommend(token):
    aid = request_all_values('aid')

    obj = MongoUser.objects(mysql_id=token['id'], activity_recommend=ObjectId(aid)).first()
    if obj is not None:
        return result_fail('已经推荐过该活动')

    # 添加活动添加数
    Activity.objects(id=aid).update(inc__statistics__recommend_count=1)
    # 添加用户推荐活动
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_recommend=ObjectId(aid))
    return result_success('推荐活动成功')


# 推荐活动 添加到活动态
@app.route("/activity/recommend/dynamic", methods=["GET", "POST"])
@filter_exception
@filter_token
def recommend_dynamic(token):
    city_id, is_friend, content, aid, pics = request_all_values('city_id', 'is_friend', 'content', 'aid', 'pics')
    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.dynamic)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)

    if is_friend == 'true':
        is_friend = True

    # 构建推荐对像
    activity = Activity(id=aid)
    activity_state = ActivityState(active_type=1, object_id=ObjectId(), content=content, pics=pic_array,
                                   activity=activity, city_id=int(city_id), is_friend=is_friend)
    # 推荐到活动态
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)

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


# 发布活动      ---------------》（添加测试数据用的，不准确的）
@app.route("/activity/issue", methods=['get'])
def issue():
    type = request.args.get("type")

    address = Address(longtitude='120.208261', latitude='30.247119', address='zhong yue', city_id=1)
    ticket1 = ActivityTicket(name='贵宾票', inventory=20, description='5月20日 周杰伦盛大演出', price=1000)
    ticket2 = ActivityTicket(name='普通票', inventory=20, description='5月20日 周杰伦盛大演出', price=200)

    ticket_into = TicketInfo(is_entity=False, contact_phone="", contact_xp_account="", tickets=[ticket1, ticket2])
    if type is None:
        creator_info = ActivityCreator(name='咕噜米', pic='1.jpg', id=1, creator_type=2)
        Activity(title="杭州体育馆，杰伦演唱会", address=address, poster='/static/imgs/activity/1.jpeg', hx_group_id='123456789',
                 labels=['旅游', '沙发'],
                 begin_time=datetime.datetime.now() + datetime.timedelta(4),
                 end_time=datetime.datetime.now() + datetime.timedelta(5),
                 creator_info=creator_info, ticket_info=ticket_into, is_free=False, cast_much='20~100').save()
    else:
        creator_info = ActivityCreator(name='咕噜米', pic='1.jpg', id=2, creator_type=1)
        Activity(title="这是  03-09 的 活动", address=address, pics=['1.jpg'], hx_group_id='123456789',
                 labels=['旅游', '沙发'], creator_info=creator_info, is_free=True,
                 queue_begin_time=[datetime.datetime.now() + datetime.timedelta(8)]).save()
    return 'ok'


# 网站上发布活动到mongo      ---------------》（添加测试数据用的，不准确的）
@app.route("/activity/issue/web", methods=['post', 'get'])
def issue_web():
    data = request_all_values('data')
    json_data = json.loads(data)
    labels = json_data['LabelNames'].split(' ')[0:len(json_data['LabelNames'].split(' ')) - 1]
    address = Address(longtitude=json_data['Address']['Log'], latitude=json_data['Address']['Lat'],
                      address=json_data['Address']['Address'], city_id=1)
    tickets = []

    cast_much = []

    for i in range(0, len(json_data['Ticket']['Tickets'])):
        ticket = ActivityTicket(name=json_data['Ticket']['Tickets'][i]['Name'],
                                inventory=json_data['Ticket']['Tickets'][i]['Num'],
                                description=json_data['Ticket']['Tickets'][i]['Des'],
                                price=json_data['Ticket']['Tickets'][i]['Price'])
        cast_much.append(float(json_data['Ticket']['Tickets'][i]['Price']))
        tickets.append(ticket)

    is_free = False if cast_much[len(cast_much) - 1] > 0 else True
    much_str = '免费' if cast_much[len(cast_much) - 1] == 0 else str(int(cast_much[0])) + '~' + str(
            int(cast_much[len(cast_much) - 1]))

    ticket_into = TicketInfo(is_entity=json_data['Ticket']['IsEntityTicket'],
                             contact_phone=json_data['Ticket']['Contact']['PhoneNum'],
                             contact_xp_account=json_data['Ticket']['Contact']['XpNum'], tickets=tickets)
    creator_info = ActivityCreator(name='咕噜米', pic='/static/imgs/user/' + str(random.randint(1, 10)) + '.jpeg', id=1,
                                   creator_type=2)

    Activity(title=json_data['Title'], address=address,
             poster='/static/imgs/activity/' + str(random.randint(1, 10)) + '.jpeg', hx_group_id='123456789',
             labels=labels,
             begin_time=datetime.datetime.strptime(
                     json_data['Time']['BeginDate'] + ' ' + json_data['Time']['BeginTime'],
                     "%Y-%m-%d %H:%M"),
             end_time=datetime.datetime.strptime(json_data['Time']['EndDate'] + ' ' + json_data['Time']['EndTime'],
                                                 "%Y-%m-%d %H:%M"),
             creator_info=creator_info, ticket_info=ticket_into, is_free=is_free, cast_much=much_str).save()
    return result_success('发布成功')


# 获取标签及标签活动    -----------------》静态数据（数据不够，后期要完善）
@app.route("/activity/label", methods=['get'])
@filter_exception
@filter_token
def activity_label(token):
    page_index = request_all_values('page_index')
    data = [{'label': '户外', 'num': 1}, {'label': '旅游', 'num': 1}, {'label': '聚会', 'num': 1}, {'label': '展览', 'num': 1},
            {'label': '骑行', 'num': 1}, {'label': '艺术', 'num': 1}]
    return result_success('成功', data)


# 获取精选活动     ----------------------》静态数据（目前做不了，后期完善）
@app.route("/activity/select", methods=['get'])
@filter_exception
@filter_token
def activity_select(token):
    page_index = request_all_values('page_index')
    data = [{'id': '123123', 'name': '户外', 'pic': '1.jpg'},
            {'id': 'qweqw2', 'name': '阳光', 'pic': '1.jpg'},
            {'id': 'sadsfdf', 'name': '时代发生的', 'pic': '1.jpg'},
            {'id': 'dfgdfgdf', 'name': '时代发生的', 'pic': '1.jpg'},
            {'id': '1231dfgdf23', 'name': '是的反弹', 'pic': '1.jpg'},
            {'id': 'dfgddfg', 'name': '翻天怪', 'pic': '1.jpg'},
            ]
    return result_success('成功', data)
