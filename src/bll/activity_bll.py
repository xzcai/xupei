# 查询活动
from bson import ObjectId

from data.database.Mongo.Activity import Activity
from data.database.Mongo.MongoUser import MongoUser


def query_activity(time, city_id, is_sponsor=True):
    if is_sponsor:
        activitys = Activity.objects(address__city_id=city_id, end_time__gle=time, creator_info__id=2).exclude(
            'tickets', 'queue_begin_time', 'pics')
    else:
        activitys = Activity.objects(address__city_id=city_id, queue_begin_time=time, creator_info__id=1).exclude(
            'tickets')
    return activitys


# 判断是否收藏该活动
def is_collection(user_id, activity_id):
    user = MongoUser.objects(mysql_id=user_id, activity_collect=activity_id).first()
    if user is None:
        return False
    else:
        return True
