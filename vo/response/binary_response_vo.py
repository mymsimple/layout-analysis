# coding: utf-8
from vo.response.base_response import BaseResponse


class BinaryResponse(BaseResponse):
    """
    二值化 结果返回报文
    """
    # 当前请求id
    sid = ''
    # 二值化之后的图片
    image = ''
