# -*- coding:utf-8 -*-

import cv2

# from idcard_recognizer.img_process.hough_liner import HoughLiner
# from idcard_recognizer.img_process.sift_detector import SiftDetector
from lsd_liner import LsdLiner
from contour_detector import ContourDetector
#from idcard_recognizer.utils import painter


from common import logger
#from common.config import Config
#DEBUG = Config().is_debug


def check_result(result):
    return False



class Recognizer(object):
    def __init__(self, img):
        self.img = img
        self.h, self.w = self.img.shape[:2]
        self.sift_points = []
        self.is_frame_ok = False
        self.four_points = []
        # self.painter = Painter(self.img)


    #     # 接收二进制的图片，预处理：灰度
    # def img_process(self):
    #     logger.debug('图片尺寸：w %d, h %d', self.w, self.h)
    #     w2h_ratio = self.w/self.h
    #     # self.img = cv2.resize(self.img, (int(1000*w2h_ratio), 1000))
    #     # self.h, self.w = self.img.shape[:2]
    #     # if DEBUG: cv2.imwrite('debug/0_resize.jpg', self.img)
    #     self.img =  cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    #
    # # 1、拉正
    # def img_rotate_by_hough(self):
    #     logger.info('进行霍夫变换检测直线')
    #     hough = HoughLiner(self.img)
    #     self.img = hough.detect_and_rotate()
    #     logger.info('完成霍夫变换旋转')
    #     if DEBUG: cv2.imwrite('debug/1rotate.jpg', self.img)
    #     return self.img
    #
    # # 2、裁切
    # def img_crop_by_sift(self):
    #     logger.info('进行sift点检测')
    #     sift = SiftDetector(self.img)
    #     self.img, self.sift_points = sift.detect_and_crop_card_area()
    #     if DEBUG: cv2.imwrite('debug/2crop.jpg', self.img)
    #     # self.sift_points = sift.points
    #
    #     logger.info('完成sift变换裁剪')
    #
    #
    # # 3、边框识别
    # def img_detect_frame_by_lsd(self):
    #     logger.info('进行lsd检测直线')
    #     lsd_liner = LsdLiner(self.img)
    #     lsd_liner.detect_lines()
    #     lsd_liner.find_frame_by_points(self.sift_points)
    #     self.is_frame_ok = lsd_liner.is_frame_ok
    #     if self.is_frame_ok:
    #         logger.info('lsd检测直线成功')
    #     else:
    #         logger.info('lsd检测直线失败，暂不使用contour法')
    #     if DEBUG and lsd_liner.is_frame_ok:
    #         painter.draw_rectangle(self.img, lsd_liner.four_points, '3lsd_frame')


     #   return lsd_liner

    # 4、跟据边框切割小图并识别
    @staticmethod
    def img_crop_and_recognize_by_lsd(lsd_liner):
        result = lsd_liner.crop_and_recognize_by_template()
        logger.info('lsd切图并识别完成')

        return result

    # 5、文字轮廓识别
    def img_crop_and_recognize_by_character_contour(self):
        contour = ContourDetector(self.img)
        result = contour.detect_and_recognize()
        logger.info('contour切图并识别完成')
        return result

    def recognize(self):
        self.img_process()
        self.img_rotate_by_hough()
        self.img_crop_by_sift()
        lsd_liner = self.img_detect_frame_by_lsd()
        if self.is_frame_ok:
            result = self.img_crop_and_recognize_by_lsd(lsd_liner)
            logger.info('识别结果：%s', result)
        else:
            result = {}
        #     if check_result(result): return result
        #     else: result = self.img_crop_and_recognize_by_character_contour()
        # else:
        #     result = self.img_crop_and_recognize_by_character_contour()

        return lsd_liner.is_frame_ok, result

if __name__ == '__main__':
    import sys
    logger.init_4_debug()

    img_path = sys.argv[1]
    #img_path = "data/correct/9.jpg"
    img = cv2.imread(img_path)
    recognizer = Recognizer(img)
    _result = recognizer.recognize()
    print(_result)
