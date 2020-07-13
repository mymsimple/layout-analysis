# coding: utf-8
from vo.response.base_response import BaseResponse,PositionEntity,WordEntity


class DetectResponse(BaseResponse):
    """
    OCR 结果返回报文
    """
    # 当前请求id
    sid = ''
    # 检测坐标信息
    detect_info = [[PositionEntity]]
    """ 页面debug用参数  """
    boxes = []
    #  划线后图片
    image = ''
    "检测后切出来的小图"
    small_images = []

