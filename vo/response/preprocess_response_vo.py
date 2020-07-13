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


class PreprocessResponse(BaseResponse):
    """
    OCR 结果返回报文
    """
    # 当前请求id
    sid = ''
    # 旋转角度
    rotate = 0
    # 矫正后的图片base64
    image = ""
