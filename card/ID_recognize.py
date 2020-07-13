# -*- coding:utf-8 -*-

import cv2
from mask_rcnn.get_mask import MaskTest
from common import logger
from mask_rcnn.config import cfg
from card.ID_template import crop_img,template_match
import logging

logger = logging.getLogger("身份证图片识别 -- 模板匹配 + local(psenet+crnn)")

# TODO:代码重构，用这个加载图片识别

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])


class Recognizer(object):
    def __init__(self,img):
        self.img = img
        self.h, self.w = self.img.shape[:2]
        self.four_points = []
        self.frame_image_path = cfg.TEST.FRAME_IMAGE_PATH
        self.approx_image_path = cfg.TEST.APPROX_IMAGE_PATH
        self.correct_image_path = cfg.TEST.CORRECT_IMAGE_PATH


     # 加载mask-rcnn模型预测，返回mask值
    def mask_rcnn(self):
        '''
        input: img
        :return: 四点坐标
        '''
        demo = MaskTest()
        point = demo.do_test(self.img)
        logger.info('mask-rcnn检测完成')
        return point


    # 判断mask区域的面积
    def area_ratio(self):

        logger.debug("mask区域面积占比:%s", )


    # 身份证正面模板匹配
    def front_template(self, point):
        warped = crop_img(self.img, point)
        final_result = template_match(warped)
        logger.debug("返回模板匹配结果:%s",final_result)
        return final_result


    # 调用local检测和识别接口
    def detect_and_recog(self):
        logger.debug("返回直接检测识别结果:%s", )




    def recognize(self):
        point = self.mask_rcnn()
        #if self.area_ratio:
        final_result = self.front_template(point)
        logger.info('识别结果：%s', final_result)
        # else:
        #     res = self.detect_and_recog(self.img)

        return final_result



if __name__ == '__main__':
    import sys
    init_logger()

    # img_path = sys.argv[1]
    # #img_path = "data/correct/9.jpg"
    # img = cv2.imread(img_path)
    recognizer = Recognizer()
    _result = recognizer.recognize()
    print(_result)
