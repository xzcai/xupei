import datetime
from functools import wraps

import time
from flask import render_template, request
from sqlalchemy.util.compat import cmp

from data.database.Mongo.City import City
from data.database.Mongo.test import TestData, Tes
from src import app
from util.image_helper import ImageHelper
from util.request_helper import request_all_values
from util.result_helper import result_fail


def deco1(func):
    @wraps
    def _deco1():
        try:
            return func()
        except Exception as e:
            print('异常错误', str(e))
            return result_fail('异常错误' + str(e))

    return _deco1


def mer():
    pics = ['C:/Users/Administrator/Desktop/img/1.jpg', 'C:/Users/Administrator/Desktop/img/2.jpg']

    return ImageHelper.sudoku_pic(pics, 'qun1')
    #
    #
    # border, position = img_test(pics)
    #
    # merge_img = Image.new('RGB', (140, 140), 0x808080)
    # for i in range(0, len(pics)):
    #     img_small = Image.open(pics[i])
    #
    #     box = clipimage(img_small.size)
    #     img_small_X = img_small.crop(box)
    #
    #     print(img_small_X)
    #
    #     img_small_X.thumbnail((border, border))
    #     img_small_X.save('C:/Users/Administrator/Desktop/' + str(i) + '1.jpg')
    #     merge_img.paste(img_small_X, position[i])
    # merge_img.save('C:/Users/Administrator/Desktop/1111111111111111.jpg', quality=70)


def img_test(pics, length=140):
    n = len(pics)
    margin = 2
    if n <= 4:
        border = int((length - margin * 3) / 2)
    else:
        border = int((length - margin * 4) / 3)
    if n == 1:
        return pics[0]
    elif n == 2:
        position = [(margin, int((length - border) / 2)), (border + 4, int((length - border) / 2))]
    elif n == 3:
        position = [(int((length - border) / 2), 2), (2, border + 4), (border + 4, border + 4)]
    elif n == 4:
        position = [(2, 2), (border + 4, 2), (2, border + 4), (border + 4, border + 4)]
    elif n == 5:
        position = [(2 + int(border / 2), (2 + int(border / 2))),
                    ((int(border / 2) + border + 4), (2 + int(border / 2))),
                    (2, (int(border / 2) + border + 4)), (border + 4, (int(border / 2) + border + 4)),
                    (2 * border + 6, (int(border / 2) + border + 4))
                    ]
    elif n == 6:
        position = [(2, int(border / 2) + 2), (border + 4, int(border / 2) + 2), (2 * border + 6, int(border / 2) + 2),
                    (2, (3 * border / 2) + 4), (border + 4, (3 * border / 2) + 4),
                    (2 * border + 6, (3 * border / 2) + 4)]
    elif n == 7:
        position = [(border + 4, 2),
                    (2, 4 + border), (border + 44 + border), (2 * border + 6, 4 + border),
                    (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]
    elif n == 8:
        position = [(int(border / 2) + 2, 2), (int(3 * border / 2) + 4, 2),
                    (2, 4 + border), (border + 4, 4 + border), (2 * border + 6, 4 + border),
                    (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]
    else:
        position = [(2, 2), (border + 4, 2), (2 * border + 6, 2),
                    (2, 4 + border), (border + 4, 4 + border), (2 * border + 6, 4 + border),
                    (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]

    return border, position


def clipimage(size):
    width = int(size[0])
    height = int(size[1])
    box = ()
    if (width > height):
        dx = width - height
        box = (int(dx / 2), 0, int(height + dx / 2), height)
    else:
        dx = height - width
        box = (0, int(dx / 2), width, int(width + dx / 2))
    return box


@app.route("/con/test")
def dd():
    return render_template('index.html')


@app.route("/test")
def testdd():
    dict = [
        {'id': '4', 'name': 'b'},
        {'id': '6', 'name': 'c'},
        {'id': '3', 'name': 'a'},
        {'id': '1', 'name': 'g'},
        {'id': '8', 'name': 'f'}
    ]

    # dict.sort(lambda x, y: cmp(x['id'], y['id']))
    dict1 = sorted(dict, key=lambda x: x['id'])

    print(dict1)
    return 'ok'


@app.route("/test1")
def test11():
    data = TestData(num=3, str_data='aaaa')
    data = TestData(num=4, str_data='aaaa')
    Tes(code='1', name='cxz', age=22, arr_list=[data, data]).save()
    return 'sdfasdfsafasf'


@app.route("/test2")
def test12():
    map_f = """
        function() {
            if(this.age>20)
                emit(this.age,{count:1})
        };
    """
    reduce_f = """
        function(key,values) {
            if(key>0)
            {
                var ret = {age:key, names:values}
                return ret
            }
        };
    """
    finalize_f = """
        function(key,values) {
            if(key>23){
                values.msg="你都25岁了"
            }
            return values
        };
    """

    list_obj = list(Tes.objects().map_reduce(map_f, reduce_f, 'inline', finalize_f=finalize_f))
    print(list_obj)

    for o in Tes.objects().map_reduce(map_f=map_f, reduce_f=reduce_f, output={'replace': 'COLLECTION_NAME'},
                                      finalize_f=finalize_f):
        print(o.key, o.value)
    return 'ok'


@app.route("/test3")
def test3():
    n,m = request_all_values('name1','name2')
    if m is None:
        print('none')
    if m:
        print('sdfsdfsdf')
    if n:
        print('123456000000')
    print(n,m)


    return '0k'


def test4():
    a=[1,3,4]

    a.append(5)
    return a


def test():
    try:
        a = 10 / 0
        print(a)
    except Exception as e:
        print(e)
    return '1111'


def city():
    citys = [{
        "pr": "香港",
        "code": "1852",
        "city": "香港"
    }, {
        "pr": "澳门",
        "code": "1852",
        "city": "澳门"
    }, {
        "pr": "北京",
        "code": "010",
        "city": "北京"
    }, {
        "pr": "上海",
        "code": "021",
        "city": "上海"
    }, {
        "pr": "天津",
        "code": "022",
        "city": "天津"
    }, {
        "pr": "重庆",
        "code": "023",
        "city": "重庆"
    }, {
        "pr": "安徽",
        "code": "0551",
        "city": "合肥"
    }, {
        "pr": "安徽",
        "code": "0553",
        "city": "芜湖"
    }, {
        "pr": "安徽",
        "code": "0556",
        "city": "安庆"
    }, {
        "pr": "安徽",
        "code": "0552",
        "city": "蚌埠"
    }, {
        "pr": "安徽",
        "code": "0558",
        "city": "亳州"
    }, {
        "pr": "安徽",
        "code": "0565",
        "city": "巢湖"
    }, {
        "pr": "安徽",
        "code": "0566",
        "city": "池州"
    }, {
        "pr": "安徽",
        "code": "0550",
        "city": "滁州"
    }, {
        "pr": "安徽",
        "code": "1558",
        "city": "阜阳"
    }, {
        "pr": "安徽",
        "code": "0559",
        "city": "黄山"
    }, {
        "pr": "安徽",
        "code": "0561",
        "city": "淮北"
    }, {
        "pr": "安徽",
        "code": "0554",
        "city": "淮南"
    }, {
        "pr": "安徽",
        "code": "0564",
        "city": "六安"
    }, {
        "pr": "安徽",
        "code": "0555",
        "city": "马鞍山"
    }, {
        "pr": "安徽",
        "code": "0557",
        "city": "宿州"
    }, {
        "pr": "安徽",
        "code": "0562",
        "city": "铜陵"
    }, {
        "pr": "安徽",
        "code": "0563",
        "city": "宣城"
    }, {
        "pr": "福建",
        "code": "0591",
        "city": "福州"
    }, {
        "pr": "福建",
        "code": "0592",
        "city": "厦门"
    }, {
        "pr": "福建",
        "code": "0595",
        "city": "泉州"
    }, {
        "pr": "福建",
        "code": "0597",
        "city": "龙岩"
    }, {
        "pr": "福建",
        "code": "0593",
        "city": "宁德"
    }, {
        "pr": "福建",
        "code": "0599",
        "city": "南平"
    }, {
        "pr": "福建",
        "code": "0594",
        "city": "莆田"
    }, {
        "pr": "福建",
        "code": "0598",
        "city": "三明"
    }, {
        "pr": "福建",
        "code": "0596",
        "city": "漳州"
    }, {
        "pr": "甘肃",
        "code": "0931",
        "city": "兰州"
    }, {
        "pr": "甘肃",
        "code": "0943",
        "city": "白银"
    }, {
        "pr": "甘肃",
        "code": "0932",
        "city": "定西"
    }, {
        "pr": "甘肃",
        "code": "0935",
        "city": "金昌"
    }, {
        "pr": "甘肃",
        "code": "0937",
        "city": "酒泉"
    }, {
        "pr": "甘肃",
        "code": "0933",
        "city": "平凉"
    }, {
        "pr": "甘肃",
        "code": "0934",
        "city": "庆阳"
    }, {
        "pr": "甘肃",
        "code": "1935",
        "city": "武威"
    }, {
        "pr": "甘肃",
        "code": "0938",
        "city": "天水"
    }, {
        "pr": "甘肃",
        "code": "0936",
        "city": "张掖"
    }, {
        "pr": "甘肃",
        "code": "0941",
        "city": "甘南"
    }, {
        "pr": "甘肃",
        "code": "1937",
        "city": "嘉峪关"
    }, {
        "pr": "甘肃",
        "code": "0930",
        "city": "临夏"
    }, {
        "pr": "甘肃",
        "code": "2935",
        "city": "陇南"
    }, {
        "pr": "广东",
        "code": "020",
        "city": "广州"
    }, {
        "pr": "广东",
        "code": "0755",
        "city": "深圳"
    }, {
        "pr": "广东",
        "code": "0756",
        "city": "珠海"
    }, {
        "pr": "广东",
        "code": "0769",
        "city": "东莞"
    }, {
        "pr": "广东",
        "code": "0757",
        "city": "佛山"
    }, {
        "pr": "广东",
        "code": "0752",
        "city": "惠州"
    }, {
        "pr": "广东",
        "code": "0750",
        "city": "江门"
    }, {
        "pr": "广东",
        "code": "0760",
        "city": "中山"
    }, {
        "pr": "广东",
        "code": "0754",
        "city": "汕头"
    }, {
        "pr": "广东",
        "code": "0759",
        "city": "湛江"
    }, {
        "pr": "广东",
        "code": "0768",
        "city": "潮州"
    }, {
        "pr": "广东",
        "code": "0762",
        "city": "河源"
    }, {
        "pr": "广东",
        "code": "0663",
        "city": "揭阳"
    }, {
        "pr": "广东",
        "code": "0668",
        "city": "茂名"
    }, {
        "pr": "广东",
        "code": "0753",
        "city": "梅州"
    }, {
        "pr": "广东",
        "code": "0763",
        "city": "清远"
    }, {
        "pr": "广东",
        "code": "0751",
        "city": "韶关"
    }, {
        "pr": "广东",
        "code": "0660",
        "city": "汕尾"
    }, {
        "pr": "广东",
        "code": "0662",
        "city": "阳江"
    }, {
        "pr": "广东",
        "code": "0766",
        "city": "云浮"
    }, {
        "pr": "广东",
        "code": "0758",
        "city": "肇庆"
    }, {
        "pr": "广西",
        "code": "0771",
        "city": "南宁"
    }, {
        "pr": "广西",
        "code": "0779",
        "city": "北海"
    }, {
        "pr": "广西",
        "code": "0770",
        "city": "防城港"
    }, {
        "pr": "广西",
        "code": "0773",
        "city": "桂林"
    }, {
        "pr": "广西",
        "code": "0772",
        "city": "柳州"
    }, {
        "pr": "广西",
        "code": "1771",
        "city": "崇左"
    }, {
        "pr": "广西",
        "code": "1772",
        "city": "来宾"
    }, {
        "pr": "广西",
        "code": "0774",
        "city": "梧州"
    }, {
        "pr": "广西",
        "code": "0778",
        "city": "河池"
    }, {
        "pr": "广西",
        "code": "0775",
        "city": "玉林"
    }, {
        "pr": "广西",
        "code": "1755",
        "city": "贵港"
    }, {
        "pr": "广西",
        "code": "1774",
        "city": "贺州"
    }, {
        "pr": "广西",
        "code": "0777",
        "city": "钦州"
    }, {
        "pr": "广西",
        "code": "0776",
        "city": "百色"
    }, {
        "pr": "贵州",
        "code": "0851",
        "city": "贵阳"
    }, {
        "pr": "贵州",
        "code": "0853",
        "city": "安顺"
    }, {
        "pr": "贵州",
        "code": "0852",
        "city": "遵义"
    }, {
        "pr": "贵州",
        "code": "0858",
        "city": "六盘水"
    }, {
        "pr": "贵州",
        "code": "0857",
        "city": "毕节"
    }, {
        "pr": "贵州",
        "code": "0855",
        "city": "黔东南"
    }, {
        "pr": "贵州",
        "code": "0859",
        "city": "黔西南"
    }, {
        "pr": "贵州",
        "code": "0854",
        "city": "黔南"
    }, {
        "pr": "贵州",
        "code": "0856",
        "city": "铜仁"
    }, {
        "pr": "海南",
        "code": "0898",
        "city": "海口"
    }, {
        "pr": "海南",
        "code": "0899",
        "city": "三亚"
    }, {
        "pr": "海南",
        "code": "0802",
        "city": "白沙县"
    }, {
        "pr": "海南",
        "code": "0801",
        "city": "保亭县"
    }, {
        "pr": "海南",
        "code": "0803",
        "city": "昌江县"
    }, {
        "pr": "海南",
        "code": "0804",
        "city": "澄迈县"
    }, {
        "pr": "海南",
        "code": "0806",
        "city": "定安县"
    }, {
        "pr": "海南",
        "code": "0807",
        "city": "东方"
    }, {
        "pr": "海南",
        "code": "2802",
        "city": "乐东县"
    }, {
        "pr": "海南",
        "code": "1896",
        "city": "临高县"
    }, {
        "pr": "海南",
        "code": "0809",
        "city": "陵水县"
    }, {
        "pr": "海南",
        "code": "1894",
        "city": "琼海"
    }, {
        "pr": "海南",
        "code": "1899",
        "city": "琼中县"
    }, {
        "pr": "海南",
        "code": "1892",
        "city": "屯昌县"
    }, {
        "pr": "海南",
        "code": "1898",
        "city": "万宁"
    }, {
        "pr": "海南",
        "code": "1893",
        "city": "文昌"
    }, {
        "pr": "海南",
        "code": "1897",
        "city": "五指山"
    }, {
        "pr": "海南",
        "code": "0805",
        "city": "儋州"
    }, {
        "pr": "河北",
        "code": "0311",
        "city": "石家庄"
    }, {
        "pr": "河北",
        "code": "0312",
        "city": "保定"
    }, {
        "pr": "河北",
        "code": "0314",
        "city": "承德"
    }, {
        "pr": "河北",
        "code": "0310",
        "city": "邯郸"
    }, {
        "pr": "河北",
        "code": "0315",
        "city": "唐山"
    }, {
        "pr": "河北",
        "code": "0335",
        "city": "秦皇岛"
    }, {
        "pr": "河北",
        "code": "0317",
        "city": "沧州"
    }, {
        "pr": "河北",
        "code": "0318",
        "city": "衡水"
    }, {
        "pr": "河北",
        "code": "0316",
        "city": "廊坊"
    }, {
        "pr": "河北",
        "code": "0319",
        "city": "邢台"
    }, {
        "pr": "河北",
        "code": "0313",
        "city": "张家口"
    }, {
        "pr": "河南",
        "code": "0371",
        "city": "郑州"
    }, {
        "pr": "河南",
        "code": "0379",
        "city": "洛阳"
    }, {
        "pr": "河南",
        "code": "0378",
        "city": "开封"
    }, {
        "pr": "河南",
        "code": "0374",
        "city": "许昌"
    }, {
        "pr": "河南",
        "code": "0372",
        "city": "安阳"
    }, {
        "pr": "河南",
        "code": "0375",
        "city": "平顶山"
    }, {
        "pr": "河南",
        "code": "0392",
        "city": "鹤壁"
    }, {
        "pr": "河南",
        "code": "0391",
        "city": "焦作"
    }, {
        "pr": "河南",
        "code": "1391",
        "city": "济源"
    }, {
        "pr": "河南",
        "code": "0395",
        "city": "漯河"
    }, {
        "pr": "河南",
        "code": "0377",
        "city": "南阳"
    }, {
        "pr": "河南",
        "code": "0393",
        "city": "濮阳"
    }, {
        "pr": "河南",
        "code": "0398",
        "city": "三门峡"
    }, {
        "pr": "河南",
        "code": "0370",
        "city": "商丘"
    }, {
        "pr": "河南",
        "code": "0373",
        "city": "新乡"
    }, {
        "pr": "河南",
        "code": "0376",
        "city": "信阳"
    }, {
        "pr": "河南",
        "code": "0396",
        "city": "驻马店"
    }, {
        "pr": "河南",
        "code": "0394",
        "city": "周口"
    }, {
        "pr": "黑龙江",
        "code": "0451",
        "city": "哈尔滨"
    }, {
        "pr": "黑龙江",
        "code": "0459",
        "city": "大庆"
    }, {
        "pr": "黑龙江",
        "code": "0452",
        "city": "齐齐哈尔"
    }, {
        "pr": "黑龙江",
        "code": "0454",
        "city": "佳木斯"
    }, {
        "pr": "黑龙江",
        "code": "0457",
        "city": "大兴安岭"
    }, {
        "pr": "黑龙江",
        "code": "0456",
        "city": "黑河"
    }, {
        "pr": "黑龙江",
        "code": "0468",
        "city": "鹤岗"
    }, {
        "pr": "黑龙江",
        "code": "0467",
        "city": "鸡西"
    }, {
        "pr": "黑龙江",
        "code": "0453",
        "city": "牡丹江"
    }, {
        "pr": "黑龙江",
        "code": "0464",
        "city": "七台河"
    }, {
        "pr": "黑龙江",
        "code": "0455",
        "city": "绥化"
    }, {
        "pr": "黑龙江",
        "code": "0469",
        "city": "双鸭山"
    }, {
        "pr": "黑龙江",
        "code": "0458",
        "city": "伊春"
    }, {
        "pr": "湖北",
        "code": "027",
        "city": "武汉"
    }, {
        "pr": "湖北",
        "code": "0710",
        "city": "襄阳"
    }, {
        "pr": "湖北",
        "code": "0719",
        "city": "十堰"
    }, {
        "pr": "湖北",
        "code": "0714",
        "city": "黄石"
    }, {
        "pr": "湖北",
        "code": "0711",
        "city": "鄂州"
    }, {
        "pr": "湖北",
        "code": "0718",
        "city": "恩施"
    }, {
        "pr": "湖北",
        "code": "0713",
        "city": "黄冈"
    }, {
        "pr": "湖北",
        "code": "0716",
        "city": "荆州"
    }, {
        "pr": "湖北",
        "code": "0724",
        "city": "荆门"
    }, {
        "pr": "湖北",
        "code": "0722",
        "city": "随州"
    }, {
        "pr": "湖北",
        "code": "0717",
        "city": "宜昌"
    }, {
        "pr": "湖北",
        "code": "1728",
        "city": "天门"
    }, {
        "pr": "湖北",
        "code": "2728",
        "city": "潜江"
    }, {
        "pr": "湖北",
        "code": "0728",
        "city": "仙桃"
    }, {
        "pr": "湖北",
        "code": "0712",
        "city": "孝感"
    }, {
        "pr": "湖北",
        "code": "0715",
        "city": "咸宁"
    }, {
        "pr": "湖北",
        "code": "1719",
        "city": "神农架"
    }, {
        "pr": "湖南",
        "code": "0731",
        "city": "长沙"
    }, {
        "pr": "湖南",
        "code": "0730",
        "city": "岳阳"
    }, {
        "pr": "湖南",
        "code": "0732",
        "city": "湘潭"
    }, {
        "pr": "湖南",
        "code": "0736",
        "city": "常德"
    }, {
        "pr": "湖南",
        "code": "0735",
        "city": "郴州"
    }, {
        "pr": "湖南",
        "code": "0734",
        "city": "衡阳"
    }, {
        "pr": "湖南",
        "code": "0745",
        "city": "怀化"
    }, {
        "pr": "湖南",
        "code": "0738",
        "city": "娄底"
    }, {
        "pr": "湖南",
        "code": "0739",
        "city": "邵阳"
    }, {
        "pr": "湖南",
        "code": "0737",
        "city": "益阳"
    }, {
        "pr": "湖南",
        "code": "0746",
        "city": "永州"
    }, {
        "pr": "湖南",
        "code": "0733",
        "city": "株洲"
    }, {
        "pr": "湖南",
        "code": "0744",
        "city": "张家界"
    }, {
        "pr": "湖南",
        "code": "0743",
        "city": "湘西"
    }, {
        "pr": "吉林",
        "code": "0431",
        "city": "长春"
    }, {
        "pr": "吉林",
        "code": "0432",
        "city": "吉林"
    }, {
        "pr": "吉林",
        "code": "1433",
        "city": "延边"
    }, {
        "pr": "吉林",
        "code": "0436",
        "city": "白城"
    }, {
        "pr": "吉林",
        "code": "0439",
        "city": "白山"
    }, {
        "pr": "吉林",
        "code": "0437",
        "city": "辽源"
    }, {
        "pr": "吉林",
        "code": "0434",
        "city": "四平"
    }, {
        "pr": "吉林",
        "code": "0438",
        "city": "松原"
    }, {
        "pr": "吉林",
        "code": "0435",
        "city": "通化"
    }, {
        "pr": "江苏",
        "code": "025",
        "city": "南京"
    }, {
        "pr": "江苏",
        "code": "0512",
        "city": "苏州"
    }, {
        "pr": "江苏",
        "code": "0519",
        "city": "常州"
    }, {
        "pr": "江苏",
        "code": "0518",
        "city": "连云港"
    }, {
        "pr": "江苏",
        "code": "0523",
        "city": "泰州"
    }, {
        "pr": "江苏",
        "code": "0510",
        "city": "无锡"
    }, {
        "pr": "江苏",
        "code": "0516",
        "city": "徐州"
    }, {
        "pr": "江苏",
        "code": "0514",
        "city": "扬州"
    }, {
        "pr": "江苏",
        "code": "0511",
        "city": "镇江"
    }, {
        "pr": "江苏",
        "code": "0517",
        "city": "淮安"
    }, {
        "pr": "江苏",
        "code": "0513",
        "city": "南通"
    }, {
        "pr": "江苏",
        "code": "0527",
        "city": "宿迁"
    }, {
        "pr": "江苏",
        "code": "0515",
        "city": "盐城"
    }, {
        "pr": "江西",
        "code": "0791",
        "city": "南昌"
    }, {
        "pr": "江西",
        "code": "0797",
        "city": "赣州"
    }, {
        "pr": "江西",
        "code": "0792",
        "city": "九江"
    }, {
        "pr": "江西",
        "code": "0798",
        "city": "景德镇"
    }, {
        "pr": "江西",
        "code": "0796",
        "city": "吉安"
    }, {
        "pr": "江西",
        "code": "0799",
        "city": "萍乡"
    }, {
        "pr": "江西",
        "code": "0793",
        "city": "上饶"
    }, {
        "pr": "江西",
        "code": "0790",
        "city": "新余"
    }, {
        "pr": "江西",
        "code": "0795",
        "city": "宜春"
    }, {
        "pr": "江西",
        "code": "0701",
        "city": "鹰潭"
    }, {
        "pr": "江西",
        "code": "0794",
        "city": "抚州"
    }, {
        "pr": "辽宁",
        "code": "024",
        "city": "沈阳"
    }, {
        "pr": "辽宁",
        "code": "0411",
        "city": "大连"
    }, {
        "pr": "辽宁",
        "code": "0412",
        "city": "鞍山"
    }, {
        "pr": "辽宁",
        "code": "0415",
        "city": "丹东"
    }, {
        "pr": "辽宁",
        "code": "0413",
        "city": "抚顺"
    }, {
        "pr": "辽宁",
        "code": "0416",
        "city": "锦州"
    }, {
        "pr": "辽宁",
        "code": "0417",
        "city": "营口"
    }, {
        "pr": "辽宁",
        "code": "0414",
        "city": "本溪"
    }, {
        "pr": "辽宁",
        "code": "0421",
        "city": "朝阳"
    }, {
        "pr": "辽宁",
        "code": "0418",
        "city": "阜新"
    }, {
        "pr": "辽宁",
        "code": "0429",
        "city": "葫芦岛"
    }, {
        "pr": "辽宁",
        "code": "0419",
        "city": "辽阳"
    }, {
        "pr": "辽宁",
        "code": "0427",
        "city": "盘锦"
    }, {
        "pr": "辽宁",
        "code": "0410",
        "city": "铁岭"
    }, {
        "pr": "内蒙古",
        "code": "0471",
        "city": "呼和浩特"
    }, {
        "pr": "内蒙古",
        "code": "0472",
        "city": "包头"
    }, {
        "pr": "内蒙古",
        "code": "0476",
        "city": "赤峰"
    }, {
        "pr": "内蒙古",
        "code": "0477",
        "city": "鄂尔多斯"
    }, {
        "pr": "内蒙古",
        "code": "0474",
        "city": "乌兰察布"
    }, {
        "pr": "内蒙古",
        "code": "0473",
        "city": "乌海"
    }, {
        "pr": "内蒙古",
        "code": "0482",
        "city": "兴安盟"
    }, {
        "pr": "内蒙古",
        "code": "0470",
        "city": "呼伦贝尔"
    }, {
        "pr": "内蒙古",
        "code": "0475",
        "city": "通辽"
    }, {
        "pr": "内蒙古",
        "code": "0483",
        "city": "阿拉善盟"
    }, {
        "pr": "内蒙古",
        "code": "0478",
        "city": "巴彦淖尔"
    }, {
        "pr": "内蒙古",
        "code": "0479",
        "city": "锡林郭勒"
    }, {
        "pr": "宁夏",
        "code": "0951",
        "city": "银川"
    }, {
        "pr": "宁夏",
        "code": "0952",
        "city": "石嘴山"
    }, {
        "pr": "宁夏",
        "code": "0954",
        "city": "固原"
    }, {
        "pr": "宁夏",
        "code": "0953",
        "city": "吴忠"
    }, {
        "pr": "宁夏",
        "code": "1953",
        "city": "中卫"
    }, {
        "pr": "青海",
        "code": "0971",
        "city": "西宁"
    }, {
        "pr": "青海",
        "code": "0973",
        "city": "黄南"
    }, {
        "pr": "青海",
        "code": "0976",
        "city": "玉树"
    }, {
        "pr": "青海",
        "code": "0975",
        "city": "果洛"
    }, {
        "pr": "青海",
        "code": "0972",
        "city": "海东"
    }, {
        "pr": "青海",
        "code": "0977",
        "city": "海西"
    }, {
        "pr": "青海",
        "code": "0974",
        "city": "海南"
    }, {
        "pr": "青海",
        "code": "0970",
        "city": "海北"
    }, {
        "pr": "山东",
        "code": "0531",
        "city": "济南"
    }, {
        "pr": "山东",
        "code": "0532",
        "city": "青岛"
    }, {
        "pr": "山东",
        "code": "0631",
        "city": "威海"
    }, {
        "pr": "山东",
        "code": "0535",
        "city": "烟台"
    }, {
        "pr": "山东",
        "code": "0536",
        "city": "潍坊"
    }, {
        "pr": "山东",
        "code": "0538",
        "city": "泰安"
    }, {
        "pr": "山东",
        "code": "0543",
        "city": "滨州"
    }, {
        "pr": "山东",
        "code": "0534",
        "city": "德州"
    }, {
        "pr": "山东",
        "code": "0546",
        "city": "东营"
    }, {
        "pr": "山东",
        "code": "0530",
        "city": "菏泽"
    }, {
        "pr": "山东",
        "code": "0537",
        "city": "济宁"
    }, {
        "pr": "山东",
        "code": "0635",
        "city": "聊城"
    }, {
        "pr": "山东",
        "code": "0539",
        "city": "临沂"
    }, {
        "pr": "山东",
        "code": "0634",
        "city": "莱芜"
    }, {
        "pr": "山东",
        "code": "0633",
        "city": "日照"
    }, {
        "pr": "山东",
        "code": "0533",
        "city": "淄博"
    }, {
        "pr": "山东",
        "code": "0632",
        "city": "枣庄"
    }, {
        "pr": "山西",
        "code": "0351",
        "city": "太原"
    }, {
        "pr": "山西",
        "code": "0355",
        "city": "长治"
    }, {
        "pr": "山西",
        "code": "0352",
        "city": "大同"
    }, {
        "pr": "山西",
        "code": "0356",
        "city": "晋城"
    }, {
        "pr": "山西",
        "code": "0354",
        "city": "晋中"
    }, {
        "pr": "山西",
        "code": "0357",
        "city": "临汾"
    }, {
        "pr": "山西",
        "code": "0358",
        "city": "吕梁"
    }, {
        "pr": "山西",
        "code": "0349",
        "city": "朔州"
    }, {
        "pr": "山西",
        "code": "0350",
        "city": "忻州"
    }, {
        "pr": "山西",
        "code": "0359",
        "city": "运城"
    }, {
        "pr": "山西",
        "code": "0353",
        "city": "阳泉"
    }, {
        "pr": "陕西",
        "code": "029",
        "city": "西安"
    }, {
        "pr": "陕西",
        "code": "0915",
        "city": "安康"
    }, {
        "pr": "陕西",
        "code": "0917",
        "city": "宝鸡"
    }, {
        "pr": "陕西",
        "code": "0916",
        "city": "汉中"
    }, {
        "pr": "陕西",
        "code": "0914",
        "city": "商洛"
    }, {
        "pr": "陕西",
        "code": "0919",
        "city": "铜川"
    }, {
        "pr": "陕西",
        "code": "0913",
        "city": "渭南"
    }, {
        "pr": "陕西",
        "code": "0910",
        "city": "咸阳"
    }, {
        "pr": "陕西",
        "code": "0911",
        "city": "延安"
    }, {
        "pr": "陕西",
        "code": "0912",
        "city": "榆林"
    }, {
        "pr": "四川",
        "code": "028",
        "city": "成都"
    }, {
        "pr": "四川",
        "code": "0816",
        "city": "绵阳"
    }, {
        "pr": "四川",
        "code": "0832",
        "city": "资阳"
    }, {
        "pr": "四川",
        "code": "0827",
        "city": "巴中"
    }, {
        "pr": "四川",
        "code": "0838",
        "city": "德阳"
    }, {
        "pr": "四川",
        "code": "0818",
        "city": "达州"
    }, {
        "pr": "四川",
        "code": "0826",
        "city": "广安"
    }, {
        "pr": "四川",
        "code": "0839",
        "city": "广元"
    }, {
        "pr": "四川",
        "code": "0833",
        "city": "乐山"
    }, {
        "pr": "四川",
        "code": "0830",
        "city": "泸州"
    }, {
        "pr": "四川",
        "code": "1833",
        "city": "眉山"
    }, {
        "pr": "四川",
        "code": "1832",
        "city": "内江"
    }, {
        "pr": "四川",
        "code": "0817",
        "city": "南充"
    }, {
        "pr": "四川",
        "code": "0812",
        "city": "攀枝花"
    }, {
        "pr": "四川",
        "code": "0825",
        "city": "遂宁"
    }, {
        "pr": "四川",
        "code": "0831",
        "city": "宜宾"
    }, {
        "pr": "四川",
        "code": "0835",
        "city": "雅安"
    }, {
        "pr": "四川",
        "code": "0813",
        "city": "自贡"
    }, {
        "pr": "四川",
        "code": "0837",
        "city": "阿坝"
    }, {
        "pr": "四川",
        "code": "0836",
        "city": "甘孜"
    }, {
        "pr": "四川",
        "code": "0834",
        "city": "凉山"
    }, {
        "pr": "西藏",
        "code": "0891",
        "city": "拉萨"
    }, {
        "pr": "西藏",
        "code": "0892",
        "city": "日喀则"
    }, {
        "pr": "西藏",
        "code": "0897",
        "city": "阿里"
    }, {
        "pr": "西藏",
        "code": "0895",
        "city": "昌都"
    }, {
        "pr": "西藏",
        "code": "0894",
        "city": "林芝"
    }, {
        "pr": "西藏",
        "code": "0896",
        "city": "那曲"
    }, {
        "pr": "西藏",
        "code": "0893",
        "city": "山南"
    }, {
        "pr": "新疆",
        "code": "0991",
        "city": "乌鲁木齐"
    }, {
        "pr": "新疆",
        "code": "0993",
        "city": "石河子"
    }, {
        "pr": "新疆",
        "code": "0995",
        "city": "吐鲁番"
    }, {
        "pr": "新疆",
        "code": "0999",
        "city": "伊犁"
    }, {
        "pr": "新疆",
        "code": "0997",
        "city": "阿克苏"
    }, {
        "pr": "新疆",
        "code": "0906",
        "city": "阿勒泰"
    }, {
        "pr": "新疆",
        "code": "0996",
        "city": "巴音"
    }, {
        "pr": "新疆",
        "code": "0909",
        "city": "博尔塔拉"
    }, {
        "pr": "新疆",
        "code": "0994",
        "city": "昌吉"
    }, {
        "pr": "新疆",
        "code": "0902",
        "city": "哈密"
    }, {
        "pr": "新疆",
        "code": "0903",
        "city": "和田"
    }, {
        "pr": "新疆",
        "code": "0998",
        "city": "喀什"
    }, {
        "pr": "新疆",
        "code": "0990",
        "city": "克拉玛依"
    }, {
        "pr": "新疆",
        "code": "0908",
        "city": "克孜勒"
    }, {
        "pr": "新疆",
        "code": "0901",
        "city": "塔城"
    }, {
        "pr": "云南",
        "code": "0871",
        "city": "昆明"
    }, {
        "pr": "云南",
        "code": "0877",
        "city": "玉溪"
    }, {
        "pr": "云南",
        "code": "0878",
        "city": "楚雄"
    }, {
        "pr": "云南",
        "code": "0872",
        "city": "大理"
    }, {
        "pr": "云南",
        "code": "0873",
        "city": "红河"
    }, {
        "pr": "云南",
        "code": "0874",
        "city": "曲靖"
    }, {
        "pr": "云南",
        "code": "0691",
        "city": "西双版纳"
    }, {
        "pr": "云南",
        "code": "0870",
        "city": "昭通"
    }, {
        "pr": "云南",
        "code": "0875",
        "city": "保山"
    }, {
        "pr": "云南",
        "code": "0692",
        "city": "德宏"
    }, {
        "pr": "云南",
        "code": "0887",
        "city": "迪庆"
    }, {
        "pr": "云南",
        "code": "0888",
        "city": "丽江"
    }, {
        "pr": "云南",
        "code": "0883",
        "city": "临沧"
    }, {
        "pr": "云南",
        "code": "0886",
        "city": "怒江"
    }, {
        "pr": "云南",
        "code": "0879",
        "city": "普洱"
    }, {
        "pr": "云南",
        "code": "0876",
        "city": "文山"
    }, {
        "pr": "浙江",
        "code": "0571",
        "city": "杭州"
    }, {
        "pr": "浙江",
        "code": "0574",
        "city": "宁波"
    }, {
        "pr": "浙江",
        "code": "0573",
        "city": "嘉兴"
    }, {
        "pr": "浙江",
        "code": "0575",
        "city": "绍兴"
    }, {
        "pr": "浙江",
        "code": "0577",
        "city": "温州"
    }, {
        "pr": "浙江",
        "code": "0580",
        "city": "舟山"
    }, {
        "pr": "浙江",
        "code": "0572",
        "city": "湖州"
    }, {
        "pr": "浙江",
        "code": "0579",
        "city": "金华"
    }, {
        "pr": "浙江",
        "code": "0578",
        "city": "丽水"
    }, {
        "pr": "浙江",
        "code": "0576",
        "city": "台州"
    }, {
        "pr": "浙江",
        "code": "0570",
        "city": "衢州"
    }]

    for i in range(0, len(citys)):
        City(id=i + 1, code=citys[i]['code'], city=citys[i]['city'], province=citys[i]['pr']).save()
    return 'ok'
