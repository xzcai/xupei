import datetime
import time


# 时间转为时间戳 obj_time 时间，如果mongo_to_now 是True 那么说明是从mongodb中取得，要减去8小时的时差
def time_to_stamp(obj_time, mongo_to_now=True):
    if mongo_to_now:
        obj_time = obj_time - datetime.timedelta(seconds=8 * 3600)
    date_str = obj_time.strftime("%Y-%m-%d %H:%M:%S")
    time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))


def time_array_to_stamp(obj_time):
    array = []
    for t in obj_time:
        date_str = t.strftime("%Y-%m-%d %H:%M:%S")
        time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        array.append(int(time.mktime(time_array)))
    return array


# 时间戳转为时间  obj_stamp:当前时间错    now_to_mongo：说明是把当前时间戳转为时间在去mong里面做比对的，就要加上8个时差
def stamp_to_time(obj_stamp, now_to_mongo=True):
    time_array = time.localtime(int(obj_stamp))
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    if now_to_mongo:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=8 * 3600)
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


# 时间添加
def time_add(obj_time, second):
    return obj_time + datetime.timedelta(second=second)
