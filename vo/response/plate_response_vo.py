#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : 车牌识别返回报文
@File    :   doc_response_vo.py    
@Author  : vin
@Time    : 2020/5/18 6:39 下午
@Version : 1.0 
'''
from vo.response.base_response import BaseResponse, PositionEntity, WordEntity

"""
错误码(code)说明：
0    --- 操作成功
9999 --- 系统异常，参考msg字段获得更多信息
1001 --- 无法在图像中找到车牌
1002 --- 车牌号码识别失败
"""


class Plate:
    plate = ""  # 车牌号
    color = "blue"  # 车牌颜色 blue
    # 车牌坐标
    position = [PositionEntity]


class DebugInfo:
    # 划线后图片 base64
    image = ''
    # 截出的车牌图片base64
    plate_image = ''


class PlateResponse(BaseResponse):
    """
    plate识别 结果返回报文
    """
    # 当前请求id
    sid = ''
    plate = Plate()
    debug_info = DebugInfo()


if __name__ == '__main__':
    resp = PlateResponse()
    plate = Plate()
    plate.plate = '12312'
    resp.plate = plate

