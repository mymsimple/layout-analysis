# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
import json
from config import cfg


def show(img, title='无标题'):
    """
    本地测试时展示图片
    :param img:
    :param name:
    :return:
    """
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname='/Users/yanmeima/workspace/ocr/crnn/data/data_generator/fonts/simhei.ttf')
    plt.title(title, fontsize='large', fontweight='bold', FontProperties=font)
    plt.imshow(img)
    plt.show()

class GetFourPoints(object):

    def __init__(self,img):
        self.img = img
        self.mask_image_path = cfg.TEST.MASK_IMAGE_PATH
        self.frame_image_path = cfg.TEST.FRAME_IMAGE_PATH
        self.approx_image_path = cfg.TEST.APPROX_IMAGE_PATH
        self.correct_image_path = cfg.TEST.CORRECT_IMAGE_PATH

        pass



    def get_approx(self):
        '''
        找轮廓，求近似四边形
        :return:
        '''
        ret, thresh = cv2.threshold(self.img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]

        # 近似四边形
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        print("epsilon:", epsilon)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        print("近似四边形的四点坐标:", approx)
        cv2.polylines(self.img, [approx], True, (0, 255, 0), 10)
        #show(img)

        # # 最小外接矩形
        # rect = cv2.minAreaRect(cnt)  # 最小外接矩形
        # box = np.int0(cv2.boxPoints(rect))  # 矩形的四个角点取整
        # cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
        # show(img)
        #
        # # 外接矩形
        # x, y, w, h = cv2.boundingRect(cnt)  # 外接矩形
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # show(img)

        return approx, img
        pass


    def format_convert(self, approx):
        pos = approx.tolist()

        points = []
        for p in pos:
            x1 = p[0][0]
            y1 = p[0][1]
            points.append([x1, y1])
        return points
        pass


    def main(self,img):
        files = os.listdir(self.mask_image_path)
        for file in files:
            img_path = os.path.join(self.mask_image_path, file)
            img = cv2.imread(img_path, 0)
            approx, img = self.get_approx(img)
            points = self.format_convert(approx)

            cv2.imwrite(os.path.join(self.approx_image_path + file), img)

            txt_path = os.path.join(self.frame_image_path + file[:-4] + ".json")
            with open(txt_path, 'w', encoding='utf-8') as json_file:
                json.dump(points, json_file, ensure_ascii=False)
        pass



if __name__ == "__main__":
    # mask_path = "./data/idcard/mask/"
    # approx_path = "./data/idcard/approx/"
    # frame_path = "./data/idcard/frame/"
    # main(mask_path, approx_path, frame_path)

    getfourpoints = GetFourPoints()
    getfourpoints.main()

    #测试
    #test4()
