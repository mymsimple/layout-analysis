"""
通用返回参数
"""


class BaseResponse:
    def __init__(self, code="0", message="success"):
        self.code = code
        self.message = message

    code = "0"
    message = "success"
    debug_info = None

    def error(self, code, message):
        self.code = code
        self.message = message


class PositionEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    x = ''
    y = ''


class WordEntity:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos
        # self.prob = prob

    word = ''  # | 是        | string   |识别结果：文本
    pos = [PositionEntity]  # | 是        | int32    |识别结果：坐标
    # prob = []   # |否        | float     |逐字置信度


class DebugInfo:
    """ 页面debug用参数 """
    boxes = []
    # 切开的小图base64
    small_images = []
    # 矫正后的文本
    text_corrected = []
    # 识别的文本
    text = []
    #  划线后图片
    image = ''
    # # 置信度
    # prob = []


if __name__ == '__main__':
    a = BaseResponse()
    print(a)
    import json
    from flask import jsonify, Flask

    app = Flask(__name__)
    app.run()
    a = BaseResponse("0", "success")
    print(a)
    b = json.dumps(a.__dict__)
    print(b)
    c = json.loads(b)
    bbb = jsonify({"a": 123})
    print(bbb)
    BaseResponse(code="9999",)