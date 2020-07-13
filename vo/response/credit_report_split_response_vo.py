# coding: utf-8
from vo.response.base_response import BaseResponse,PositionEntity,WordEntity


class SplitResponse(BaseResponse):
    """
        征信报告预处理拆分结果
    """
    # 当前请求id
    sid = ''
    # 预处理后的大图
    image = ""
    # 旋转的角度
    rotate_angle = 0
    # 拆分后的图片，可能拆分成一张或两张图片
    split_images = []
    # 拆分位置
    split_width = 0
