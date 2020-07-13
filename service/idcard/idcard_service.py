#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# ============================================
# @Time     : 2020/05/18 14:42
# @Author   : WanDaoYi
# @FileName : mask_test.py
# ============================================

from datetime import datetime
import os
import cv2
import numpy as np
from mask_rcnn.m_rcnn.mask_rcnn import MaskRCNN
from card.ID_template import crop_img, template_match
from mask_rcnn.config import cfg
import logging

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from server.conf import system_config

logger = logging.getLogger("身份证图片识别 -- 模板匹配 + local(psenet+crnn)")


def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])


class MaskTest(object):
    #
    # def __init__(self):
    #
    #     # 获取 类别 list
    #     #TODO !! 分类数据
    #     self.class_names_path = cfg.COMMON.COCO_CLASS_NAMES_PATH
    #     # self.class_names_path = cfg.COMMON.OUR_CLASS_NAMES_PATH
    #     self.class_names_list = self.read_class_name()
    #
    #     # 测试图像的输入和输出路径
    #     self.test_image_file_path = cfg.TEST.TEST_IMAGE_FILE_PATH
    #     self.output_image_path = cfg.TEST.OUTPUT_IMAGE_PATH
    #     self.cut_image_path = cfg.TEST.CUT_IMAGE_PATH
    #     self.mask_image_path = cfg.TEST.MASK_IMAGE_PATH
    #     self.frame_image_path = cfg.TEST.FRAME_IMAGE_PATH
    #     self.approx_image_path = cfg.TEST.APPROX_IMAGE_PATH
    #     self.correct_image_path = cfg.TEST.CORRECT_IMAGE_PATH
    #
    #     # 加载网络模型
    #     self.mask_model = MaskRCNN(train_flag=False)
    #     # 加载权重模型
    #     self.mask_model.load_weights(cfg.TEST.COCO_MODEL_PATH, by_name=True)
    #     pass

    @staticmethod
    def cut_rectangle(results_info_list):
        '''
        抠出外接矩形
        '''
        # box = results_info_list[0]['rois']
        # ymin = box[0][0]
        # xmin = box[0][1]
        # ymax = box[0][2]
        # xmax = box[0][3]
        # w = xmax - xmin
        # h = ymax - ymin
        # cut_img = image_info[ymin:ymin + h, xmin:xmin + w]

        masks = results_info_list[0]['masks']
        binary = masks * 255
        # binary = (masks-1) * (-255) # 黑白颜色对换
        binary = np.array(binary)
        binary = binary.reshape(len(binary), -1)
        binary = binary.astype(np.uint8)
        # mask_path = os.path.join(self.mask_image_path + test_image_name)
        # cv2.imwrite(mask_path, binary)

        # 找轮廓，求近似四边形
        im2, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # logger.info("近似四边形的四点坐标:%s", approx)
        # cv2.polylines(binary, [approx], True, (0, 255, 0), 10)
        # cv2.imwrite("data/idcard/test.jpg", binary)

        return approx
        pass

    @staticmethod
    def format_convert(approx):
        pos = approx.tolist()
        points = []
        for p in pos:
            x1 = p[0][0]
            y1 = p[0][1]
            points.append([x1, y1])
        logger.debug("转换格式后的近似四边形的四点坐标:%s", points)
        return points
        pass

    # 身份证正面模板匹配
    @staticmethod
    def front_template(point, image_info):
        point = np.array(point)
        warped = crop_img(image_info, point)
        result = template_match(warped)
        logger.debug("返回模板匹配结果:%s", result)
        return result
        pass

    def recognize(self, point, image_info):
        # if self.area_ratio:
        _result = self.front_template(point, image_info)
        # else:
        #     res = self.detect_and_recognize(self.img)
        logger.info('最终识别结果:%s', _result)
        return _result
        pass

    def area_ratio(self):
        logger.info()


from service.m_rcnn.mask_rcnn_service import MaskRCNN


def process(image):
    mask_rcnn_call = MaskRCNN()

    results_info_list = mask_rcnn_call.detect([image], params=system_config.table_detect_params.model_params,
                                              mode='single',
                                              mode_name="demo")
    logger.info("mask-rcnn返回结果: {}".format(results_info_list))

    test = MaskTest()
    approx = test.cut_rectangle(results_info_list)
    # cv2.imwrite(os.path.join(self.cut_image_path + test_image_name), cut_img)
    point = test.format_convert(approx)
    final_result = test.recognize(point, image)
    return final_result


if __name__ == "__main__":
    init_logger()

    # 代码开始时间
    start_time = datetime.now()
    print("开始时间: {}".format(start_time))

    demo = MaskTest()
    demo.do_test()

    # 代码结束时间
    end_time = datetime.now()
    print("结束时间: {}, 测试模型耗时: {}".format(end_time, end_time - start_time))
