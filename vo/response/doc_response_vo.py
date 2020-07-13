#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : 合同识别返回报文
@File    :   doc_response_vo.py    
@Author  : vin
@Time    : 2020/5/18 6:39 下午
@Version : 1.0 
'''
from vo.response.base_response import BaseResponse, PositionEntity, WordEntity


class RowEntity:
    """
     行报文
    """

    def __init__(self, word, pos, row_type, word_info):
        self.word = word
        self.pos = pos
        self.type = row_type
        self.word_info = word_info

    word = ''  # | 是        | string   |识别结果：文本
    pos = [PositionEntity]  # | 是        | int32    |识别结果：坐标
    row_type = 'text'  # | 是        | string   |行类型：文本，表格
    word_info = [WordEntity]


class DebugInfo:
    """ TODO 页面debug用参数 TODO  """
    boxes = []
    # 切开的小图base64
    small_images = []
    # 矫正后的文本
    text_corrected = []
    # 识别的文本
    text = []
    #  划线后图片
    image = ''


class DocResponse(BaseResponse):
    """
    合同识别 结果返回报文
    """
    # 当前请求id
    sid = ''
    # 版本
    prism_version = ''
    # 识别结果的长度
    prism_wnum = ''
    prism_rowsInfo = [RowEntity]  # | 是        | array()  |识别结果：分行的坐标和文本|

    height = ''  # | 是        | int32    | 要识别图片的高           |
    width = ''  # | 是        | int32    | 要识别图片的宽           |
    orgHeight = ''  # | 否        | int32    | 要识别图片的高           |
    orgWidth = ''  # | 否        | int32    | 要识别图片的宽           |
    content = []  # | 否        | array()  | 识别后的文本             |
    debug_info = DebugInfo()

"""
返回报文示例：
{
    "sid": "6c8f999fe943bd5ad325483fb860a3f0645e9b214bdffb4b6a4d9ae96ea9debb6b861c69",
    "prism_version": "1.0.9",
    "prism_wnum": 182,
    "prism_rowsInfo": [
        {
            "word": "3.1债券资产登记服务",
            "pos": [{"x": 340, "y": 46}, {"x": 582, "y": 46}, {"x": 582, "y": 72}, {"x": 340, "y": 72}],
            "type": "text",
            "wordInfo": [
                {
                    "word": "3.1",
                    "pos": [{"x": 340, "y": 46}, {"x": 582, "y": 46}, {"x": 582, "y": 72}, {"x": 340, "y": 72}]
                },
                {
                    "word": "债券资产登记服务",
                    "pos": [{"x": 602, "y": 44}, {"x": 836, "y": 40}, {"x": 837, "y": 68}, {"x": 602, "y": 71}]
                }]
        },
        {
            "word": "",
            "pos": [{"x": 340, "y": 46}, {"x": 582, "y": 46}, {"x": 582, "y": 72}, {"x": 340, "y": 72}],
            "type": "table",
            "wordInfo": [
            ]
        }
    ],

    "height": 1200,
    "width": 1600,
    "orgHeight": 1200,
    "orgWidth": 1600,
    "content": "3.1债券资产登记服务 仅供审核使用 核实图片 2峂 201311300746 3 ...."
}

"""
