# 活动态  动态
from bson import ObjectId

from data.database.Mongo.DynamicComment import DynamicComment
from data.database.Mongo.MongoUser import MongoUser, Interrupt, MessageInfo
from src import app
from util.decorator_helper import filter_exception
from util.request_helper import request_all_values
from util.result_helper import result_success
from util.time_helper import time_to_stamp
from util.token_helper import filter_token


# 根据活动态id 获取活动态评论
def get_comment(dynamic_id):
    data = []
    for comment in DynamicComment.objects(dynamic_id=dynamic_id):
        com = {
            'id': str(comment.id),
            'my_name': comment.ori_user.info.nickname,
            'my_pic': comment.ori_user.info.pic,
            'obj_name': comment.obj_user.info.nickname if False else '',
            'content': comment.content,
            'add_time': time_to_stamp(comment.add_time)
        }
        data.append(com)
    return data


# 根据用户点赞数组，获取活动态点赞信息
def get_raise(raise_array, uid):
    is_raise = False
    pics = []
    length = len(raise_array)
    for i in range(0, length):
        if i < 10:
            pics.append(raise_array[i].info.pic)
        if raise_array[i].mysql_id == uid:
            is_raise = True
    return {'num': length, 'is_raise': is_raise, 'pics': pics}


# 获取活动态数据分页(查看自己和好友的)
@app.route("/dynamic", methods=['GET'])
@filter_exception
@filter_token
def dynamic(token):
    page_index, page_size = request_all_values('page_index', 'page_size')
    page_index = int(page_index if page_index is not None else 1)
    page_size = int(page_size if page_size is not None else 10)
    uid = token['id']
    obj = list(MongoUser.objects(mysql_id=uid).only('friends').first().friends)
    obj.append(uid)

    active_state = []
    obj = MongoUser.objects(mysql_id__in=obj).order_by('-activity_state__add_time').only('activity_state', 'info')
    for user in obj:
        length = len(user.activity_state)
        if length > 0:
            for i in range(0, length):
                dynamic = user.activity_state[i]
                data = {
                    'id': str(dynamic.object_id),
                    'user_info': {'name': user.info.nickname, 'pic': user.info.pic, 'id': user.mysql_id},
                    'activity': {'id': str(dynamic.activity.id if dynamic.activity is not None else ''),
                                 'title': dynamic.activity.title if dynamic.activity is not None else '',
                                 'address': dynamic.activity.address.address if dynamic.activity is not None else ''},
                    'content': dynamic.content if dynamic.content is not None else '',
                    'pics': dynamic.pics,
                    'add_time': time_to_stamp(dynamic.add_time),
                    'type': dynamic.active_type,
                    'comments': {'num': 12, 'content': ''},
                    'interrupt': {'content': dynamic.interrupt.content if dynamic.interrupt is not None else '',
                                  'add_time': time_to_stamp(
                                          dynamic.interrupt.add_time) if dynamic.interrupt is not None else '',
                                  'uid': dynamic.interrupt.user_id.mysql_id if dynamic.interrupt is not None else '',
                                  'name': dynamic.interrupt.user_id.info.nickname if dynamic.interrupt is not None else '',
                                  },
                    'raise': get_raise(dynamic.raise_up, uid),
                    'log': dynamic.longitude if dynamic.longitude is not None else '',
                    'lat': dynamic.latitude if dynamic.latitude is not None else '',
                    'address': dynamic.address if dynamic.address is not None else '',
                    'begin_time': dynamic.begin_time if dynamic.begin_time is not None else ''
                }
                active_state.append(data)

    result = sorted(active_state, key=lambda x: x['add_time'], reverse=True)
    return result_success('获取数据成功', result[(page_index - 1) * page_size:page_index * page_size])


# 获取活动态最新动态数
@app.route("/dynamic/new/num", methods=['GET'])
@filter_exception
@filter_token
def get_new_num(token):
    user = MongoUser.objects(mysql_id=token['id']).only('message_info').first()
    return result_success('成功', len(user.message_info))


# 获取活动态最新动态信息
@app.route("/dynamic/new/info", methods=['GET'])
@filter_exception
@filter_token
def get_new_info(token):
    data = []
    user = MongoUser.objects(mysql_id=token['id']).only('message_info').first()
    for obj in user.message_info:
        msg = {
            'id': obj.user.mysql_id,
            'add_time': time_to_stamp(obj.add_time),
            'type': obj.type,
            'name': obj.user.info.nickname,
            'pic': obj.user.info.pic
        }
        data.append(msg)
    return result_success('成功', data)


# 添加删除 插话
@app.route("/dynamic/interrupt", methods=['GET', 'POST'])
@filter_exception
@filter_token
def add_interrupt(token):
    content, dynamic_id, op = request_all_values('content', 'dynamic_id', 'op')
    user = MongoUser(mysql_id=token['id'])
    if op == 'add':
        interrupt = Interrupt(content=content, user_id=token['id'])
        message_info = MessageInfo(user=user, type=1)
        MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(
                set__activity_state__S__interrupt=interrupt, add_to_set__message_info=message_info)
    else:
        MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update_one(
                unset__activity_state__S__interrupt=1)
    return result_success('成功')


# 点赞，取消点赞
@app.route("/dynamic/raise", methods=['GET', 'POST'])
@filter_exception
@filter_token
def add_raise(token):
    dynamic_id, uid, op = request_all_values('dynamic_id', 'uid', 'op')
    user = MongoUser(mysql_id=token['id'])
    if op == 'add':
        message_info = MessageInfo(user=user, type=2)
        # MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(**{'add_to_set__activity_state__$__raise_up':user})
        # 第二种写法（点赞的同时，要将提示信息也插入到用户messge_info中） 如果自己对自己点赞则不加入消息提示中
        if int(uid) == token['id']:
            MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(
                    add_to_set__activity_state__S__raise_up=user)
        else:
            MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(
                    add_to_set__activity_state__S__raise_up=user, add_to_set__message_info=message_info)
    else:
        # 注意 当有外键引用时，插入可以直接插入id，删除却要用document
        MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(
                **{'pull__activity_state__$__raise_up': user})
    return result_success('成功')


# 添加评论
@app.route("/dynamic/comment/post", methods=['get', 'POST'])
@filter_exception
@filter_token
def add_comment(token):
    obj_uid, dynamic_uid, dynamic_id, content = request_all_values('obj_uid', 'dynamic_uid', 'dynamic_id', 'content')
    ori_user = MongoUser(mysql_id=token['id'])
    obj_user = MongoUser(mysql_id=obj_uid)
    DynamicComment(dynamic_id=ObjectId(dynamic_id), content=content, ori_user=ori_user, obj_user=obj_user).save()
    message_info = MessageInfo(user=ori_user, type=4)
    if int(dynamic_uid) != token['id']:
        MongoUser.objects(activity_state__object_id=ObjectId(dynamic_id)).update(add_to_set__message_info=message_info)
    return result_success('添加成功')


# 删除评论
@app.route("/dynamic/comment", methods=['DELETE'])
@filter_exception
@filter_token
def delete_comment(token):
    comment_id = request_all_values('comment_id')
    DynamicComment.objects(id=comment_id, ori_user=token['id']).delete()
    return result_success('删除成功')


# 获取评论
@app.route("/dynamic/comment", methods=['GET'])
@filter_exception
@filter_token
def get_comment(token):
    dynamic_id = request_all_values('dynamic_id')
    comments = []
    for comment in DynamicComment.objects(dynamic_id=dynamic_id):
        data = {
            'ori_uid': comment.ori_user.mysql_id,
            'ori_pic': comment.ori_user.info.pic,
            'ori_nickname': comment.ori_user.info.nickname,
            'obj_uid': comment.obj_user.mysql_id if comment.obj_user.id != 0 else 0,
            'obj_nickname': comment.obj_user.info.nickname if comment.obj_user.id != 0 else '',
            'add_time': time_to_stamp(comment.add_time),
            'content': comment.content
        }
        comments.append(data)
    return result_success('成功', comments)


# 用户删除自己的 删除活动态
@app.route("/dynamic/delete", methods=['GET', 'DELETE'])
@filter_exception
@filter_token
def dynamic_delete(token):
    dynamic_id = request_all_values('dynamic_id')
    MongoUser.objects(mysql_id=token['id']).update_one(pull__activity_state__object_id=ObjectId(dynamic_id))
    return result_success('删除成功')
