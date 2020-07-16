import logging
import cv2
import numpy as np
import sys


"""
检测类服务，对外提供统一的文本检测服务，目前包含功能：
1.ctpn检测
2.psenet检测
3.doc传统图像法检测
使用方法：

"""
logger = logging.getLogger(__name__)


# TODO 对外提供的模型应该自定义，隐藏内部实现敏感信息

def draw_image(image, boxes, draw=False, color=(0, 0, 255)):
    """
    :param image: 要画的图片
    :param boxes:  应该是n,4,2格式
    :param draw:  是否画框
    :return:
    """
    if not draw:
        return None
    # TODO 随机选一个颜色
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            draw_box = np.array(box).reshape((-1, 2))
            # print("要画的框：", draw_box)
            cv2.polylines(image, np.int32([draw_box]), color=color, thickness=1, isClosed=True)
    return image


def draw_rect(image, boxes, draw=False):
    if not draw:
        return None
    if len(boxes) == 0:
        return image
    for box in boxes:
        box = box.astype(np.int32)
        cv2.rectangle(image,
                      (box[0], box[1]),
                      (box[2], box[3]),
                      color=(0, 255, 0),
                      thickness=1)
    return image
