from src import app


# 创建队列
@app.route("/queue/create", methods=["GET", "POST"])
def queue_create():
    pass


# 创建队列活动
@app.route("/queue/activity", methods=["POST"])
def queue_create_activity():
    pass


# 获取队列详情
@app.route("/queue/detail", methods=["GET"])
def queue_detail():
    pass


# 获取队列活动
@app.route("/queue/activity")
def queue_activity():
    pass


# 获取队列相册
@app.route("/queue/photo")
def queue_photo():
    pass


# 获取队列成员
@app.route("/queue/member")
def queue_member():
    pass


# 移除成员
@app.route("/queue/member", methods=["GET","DELETE"])
def queue_delete_member():
    pass


# 添加成员
@app.route("/queue/member", methods=["GET","POST"])
def queue_add_member():
    pass


# 设置副队
@app.route("/queue/deputy",methods=["GET","PUT"])
def queue_set_deputy():
    pass


