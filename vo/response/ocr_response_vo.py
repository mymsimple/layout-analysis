# coding: utf-8
from vo.response.base_response import BaseResponse, PositionEntity, WordEntity


# from vo.response.base_response import BaseResponse,PositionEntity,WordEntity,ProbEntity


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


class OcrResponse(BaseResponse):
    """
    OCR 结果返回报文
    """
    # 当前请求id
    sid = ''
    # 版本
    prism_version = ''
    # 识别结果的长度
    prism_wnum = ''
    prism_wordsInfo = [WordEntity]  # | 是        | array()  |识别结果：未分行的坐标和文本|
    prism_wordsInfo_row = [[WordEntity]]  # | 是        | array()  |识别结果：分行后的坐标和文本|
    # 表格检测结果
    table_info = [[PositionEntity]]

    height = ''  # | 是        | int32    | 要识别图片的高           |
    width = ''  # | 是        | int32    | 要识别图片的宽           |
    orgHeight = ''  # | 否        | int32    | 要识别图片的高           |
    orgWidth = ''  # | 否        | int32    | 要识别图片的宽           |
    content = []  # | 否        | array()  | 识别后的文本             |
    debug_info = DebugInfo()


"""
     返回示例
    {
        "sid":"6c8f999fe943bd5ad325483fb860a3f0645e9b214bdffb4b6a4d9ae96ea9debb6b861c69",
        "prism_version":"1.0.9",
        "prism_wnum":182,
        "prism_wordsInfo":[
        {
            "word":"供审核使用",
            "pos":[{"x":340,"y":46},{"x":582,"y":46},{"x":582,"y":72},{"x":340,"y":72}]
        },
        {
            "word":"核实图片",
            "pos":[{"x":602,"y":44},{"x":836,"y":40},{"x":837,"y":68},{"x":602,"y":71}]
        }],
        "prism_wordsInfo_row":
        [  
            [ {
                    "word":"供审核使用",
                    "pos":[{"x":340,"y":46},{"x":582,"y":46},{"x":582,"y":72},{"x":340,"y":72}]
                },{
                    "word":"核实图片",
                    "pos":[{"x":602,"y":44},{"x":836,"y":40},{"x":837,"y":68},{"x":602,"y":71}]
              } ],
            [ {
                    "word":"供审核使用",
                    "pos":[{"x":340,"y":46},{"x":582,"y":46},{"x":582,"y":72},{"x":340,"y":72}]
                },{
                    "word":"核实图片",
                    "pos":[{"x":602,"y":44},{"x":836,"y":40},{"x":837,"y":68},{"x":602,"y":71}]
              } ],
            ....
        ],

        "height":1200,
        "width":1600,
        "orgHeight":1200,
        "orgWidth":1600,
        "content":"仅供审核使用 核实图片 2峂 201311300746 3 ...."
    }
"""

if __name__ == '__main__':
    response = OcrResponse()
    response.sid = "6c8f999fe943bd5ad325483fb860a3f0645e9b214bdffb4b6a4d9ae96ea9debb6b861c69"
    response.prism_version = "1.0.9"
    response.prism_wnum = 182
    word1 = WordEntity("whew", [PositionEntity(10, 120)])
    word2 = WordEntity("word2", [PositionEntity(10, 120)])
    response.prism_wordsInfo = [word1, word2]
    response.prism_wordsInfo_row = [[word1, word2]]

    response.height = 1200
    response.width = 1600
    response.orgHeight = 1200
    response.orgWidth = 1600
    response.content = ["仅供审核使用 核实图片 2峂 201311300746 3 ....", "helweo"]
    import json

    print("hello")
    from flask import Response

    json_str = json.dumps(response, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    res = Response(json_str, content_type='application/json')
    # .decode("utf-8").encode("gb2312")
    from flask import jsonify

    test = jsonify(json_str)
    print(json_str)
