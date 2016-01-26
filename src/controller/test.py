from functools import wraps

from PIL import Image

from src import app
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

    pics = ['C:/Users/Administrator/Desktop/img/a1.jpg', 'C:/Users/Administrator/Desktop/img/a1.jpg',
            'C:/Users/Administrator/Desktop/img/a1.jpg', 'C:/Users/Administrator/Desktop/img/a1.jpg',
            'C:/Users/Administrator/Desktop/img/a1.jpg', 'C:/Users/Administrator/Desktop/img/a1.jpg',
            'C:/Users/Administrator/Desktop/img/a1.jpg', 'C:/Users/Administrator/Desktop/img/a1.jpg',
            'C:/Users/Administrator/Desktop/img/a1.jpg']
    post = [(0, 0), (0, 40), (0, 80),
            (40, 0), (40, 40), (40, 80),
            (80, 0), (80, 40), (80, 80)]
    merge_img = Image.new('RGB', (120, 120), 0x808080)
    for i in range(0, len(pics)):
        img_small = Image.open(pics[i])

        # box = clipimage(img_small.size)
        # img_small_X = img_small.crop(box)

        img_small.thumbnail((40, 40), Image.ANTIALIAS)
        img_small.save('C:/Users/Administrator/Desktop/' + str(i) + '1.jpg')
        merge_img.paste(img_small, post[i])
        merge_img.save('C:/Users/Administrator/Desktop/' + str(i) + '.jpg', quality=70)
    merge_img.save('C:/Users/Administrator/Desktop/1111111111111111.jpg', quality=70)


def clipimage(size):
    width = int(size[0])
    height = int(size[1])
    box = ()
    if (width > height):
        dx = width - height
        box = (dx / 2, 0, height + dx / 2, height)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box


@app.route("/con/test")
def dd():
    mer()
    # watermark('C:/Users/Administrator/Desktop/img/a1.jpg', 'C:/Users/Administrator/Desktop/img/a1.jpg')
    return 'ok'


def test():
    pass
    # data = [{'id':1,'uid': 1, 'pid': 0, 'content': 'nihao'}, {'uid': 2, 'pid': 0, 'content': 'nihao'},
    #         {'uid': 1, 'pid': 0, 'content': 'nihao'}, {'uid': 1, 'pid': 0, 'content': 'nihao'}]
