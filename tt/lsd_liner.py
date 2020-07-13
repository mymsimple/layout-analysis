# -*- coding:utf-8 -*-

'''
找框法识别身份证
'''
from common.config import Config
DEBUG = Config().is_debug

import cv2
import math
import numpy as np
import sys
from common import logger
#from idcard_recognizer.utils import painter, img2string
if DEBUG: sys.path.append('/Users/tt/CV/ocr_card/idcard')


idcard_w2h_ratio = 8.56/5.4  # 身份证长宽比

# 两点距离
def distance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

# 两点拟合一条直线
def fit_line(points):
    # fit a line ax+by+c = 0
    # points:[[x0,x1],[y0,y1]]
    p1 = points[0]
    p2 = points[1]
    if p1[0] == p1[1]:
        return [1., 0., -p1[0]]
    else:
        [k, b] = np.polyfit(p1, p2, deg=1)
        k, b = round(k, 2), round(b, 2)
        return [k, -1., b]

# 求两条直线的交点
def line_cross_point(line1, line2):
    # line1 0= ax+by+c, compute the cross point of line1 and line2
    if line1[0] != 0 and line1[0] == line2[0]: #k,也就是斜率一样，两条线平行啊，没交叉点啊!!!
        logger.debug('Cross point does not exist')
        return None
    if line1[0] == 0 and line2[0] == 0: # 都是平行于x轴，没交叉点啊!!!
        logger.debug('Cross point does not exist')
        return None
    if line1[1] == 0:
        x = -line1[2]
        y = line2[0] * x + line2[2]
    elif line2[1] == 0:
        x = -line2[2]
        y = line1[0] * x + line1[2]
    else: # 这个才是求那个点呢，这个是解一个2元1次方程组得到的，就是x1=x2,y1=y2，方程就是成了 y1=x1*k1+b1 ~ y1=x1*k2+b2，解出，x1,y1
        k1, _, b1 = line1
        k2, _, b2 = line2
        x = -(b1-b2)/(k1-k2) # 求解交叉点
        y = k1*x + b1
    return [x, y]

# 按照斜率，将画面内所有的线分成2拨：竖线（k∈[-∞,-1]∪[1，∞]），横线（k∈[-1，1]）
def distinct_horizontal_and_vertical(lines, w, h):
    '''
    :param lines: [[-56.75, -1.0, 29469.75], [-0.07, -1.0, 380.77]]
    :return:dict:{0:[[-0.07, -1.0, 380.77]],1:[[-56.75, -1.0, 29469.75]]}
    '''
    lines_by_direction = {0:[], 1:[]}  #0:水平的, 1:竖直的
    epsilon = 0.0000001

    for line_p in lines:
        [x0, y0, x1, y1] = line_p
        line = fit_line(((x0, x1), (y0, y1)))
        k = -line[0]/(line[1]+epsilon)
        if -1 < k < 1:
            if distance(x0, y0, x1, y1) < w * 0.3: continue
            lines_by_direction[0].append(line)
            logger.debug('直线是横线 %s', line)
        else:
            if distance(x0, y0, x1, y1) < h * 0.3: continue
            lines_by_direction[1].append(line)
            logger.debug('直线是竖线 %s', line)

    return lines_by_direction

# 将横线、竖线分别按照顺序排列。横线：b(C)从小到大，竖线：直线在x轴的截距，从小到大
def order_lines(lines):
    lines[0] = sorted(lines[0],key=lambda oneline: oneline[2])  # 默认reverse = False 升序
    lines[1] = sorted(lines[1],key=lambda oneline: -oneline[2]/oneline[0])
    return lines

# 对siftpoints，删掉离群值：先算出每个点距离平均点的距离。再求出距离的平均值、标准差。3δ 检验|l-l0|/δ >2 抛弃
def delete_outliers(points):
    center_point = np.average(points,axis=0)   # 中心点的坐标,(x0,y0)
    distances = [ distance(center_point[0],center_point[1],point[0],point[1]) for point in points ]
    ave_dist = np.average(distances)
    std_dist = np.std(distances)
    points_new = points.copy()
    # print(points_new)
    for i,point in enumerate(points):
        # print(i,point)
        if abs(distances[i]-ave_dist)/std_dist >2:
            points_new.remove(point)
            # print('num of points left:',len(points_new))
            # print('deleted:',point)

    return points_new

# 横线的y值
def y_value(line,x):
    epsilon = 0.00001
    return round(-(line[2]+line[0]*x)/(line[1]+epsilon),2)

# 纵线的x值
def x_value(line,x):
    epsilon = 0.00001
    return round(-(line[2]+line[1]*x)/(line[0]+epsilon),2)

# 求出选定的4条线的交点，即我们要找的4个点
def get_four_intersaction_points(lines):
    points = [line_cross_point(lines[0], lines[2]),
              line_cross_point(lines[0], lines[3]),
              line_cross_point(lines[1], lines[3]),
              line_cross_point(lines[1], lines[2])
              ]
    return points


class LsdLiner(object):
    def __init__(self, img):
        self.img = img
        self.h, self.w = img.shape[:2]
        self.lines = []
        self.four_points = []
        self.is_frame_ok = False

    def detect_lines(self):
        # _, self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # if DEBUG: cv2.imwrite('debug/3.0binary.jpg', self.img)

        logger.debug('lsd1')
        lsd = cv2.createLineSegmentDetector(0)
        logger.debug('lsd2')
        logger.info('开始进行lsd检测')

        lines = lsd.detect(self.img)[0]
        logger.debug('lsd3')
        original_lines = []
        filtered_lines = []
        candidate_lines = []

        for dline in lines:
            x0 = int(round(dline[0][0]))
            y0 = int(round(dline[0][1]))
            x1 = int(round(dline[0][2]))
            y1 = int(round(dline[0][3]))
            original_lines.append([x0, y0, x1, y1])
            # if distance(x0,y0,x1,y1)< self.w*0.2: continue
            # filtered_lines.append([x0, y0, x1, y1])

            candidate_lines.append([x0, y0, x1, y1])   # [[x0, y0, x1, y1],[x0, y0, x1, y1]]

        if DEBUG:
            painter.draw_line_by_lines(self.img, original_lines, '3.1lsd_lines_1')
            painter.draw_line_by_lines(self.img, filtered_lines, '3.1lsd_lines_2')
        logger.info('lsd 一共检测出【%d】条直线，长度过滤后为【%d】条竖线', len(original_lines), len(filtered_lines))

        self.lines = order_lines(distinct_horizontal_and_vertical(candidate_lines, self.w, self.h))

        logger.info('lsd 检测出【%d】条横线，【%d】条竖线', len(self.lines[0]), len(self.lines[1]))

        return self.lines

    # 找出最合适的轮廓：对每个sift发现的点，求出包围它最小的框（2条横线，2条竖线）。然后求出包围所有点的最小的框（2条横线，2条竖线）
    def find_frame_by_points(self, points):
        '''
        :param points: sift发现的关键点
        :return: 身份证边框4条直线方程
        '''

        # painter.draw_points(self.img, points, 'sift_point')
        aim_line_indexes = {0: set(), 1: set()}
        for point in points:
            x0 = point[0]
            y0 = point[1]
            # 找最近的两条横线，先求出所有横线的yn，然后找到y0前后的2个yn，然后根据value对应回横线index
            yn = [y_value(line, x0) for line in self.lines[0]]  # 图上所有横线 被切到的纵坐标
            yn_sorted = sorted(yn + [y0])
            if yn_sorted.index(y0) + 1 <= len(yn_sorted) - 1:  # 防止index out of range
                aim_line_indexes[0].add(yn.index(yn_sorted[yn_sorted.index(y0) + 1]))
            if yn_sorted.index(y0) - 1 >= 0:
                aim_line_indexes[0].add(yn.index(yn_sorted[yn_sorted.index(y0) - 1]))
            # 找到最近的两条竖线
            xn = [x_value(line, y0) for line in self.lines[1]]  # 图上所有纵线 被切到的横坐标
            xn_sorted = sorted(xn + [x0])
            if xn_sorted.index(x0) + 1 <= len(xn_sorted) - 1:  # 防止index out of range
                aim_line_indexes[1].add(xn.index(xn_sorted[xn_sorted.index(x0) + 1]))
            if xn_sorted.index(x0) - 1 >= 0:
                aim_line_indexes[1].add(xn.index(xn_sorted[xn_sorted.index(x0) - 1]))

        # 如果没有找到线，就返回所有的线（防止min()max()函数报错，暂时这么做一下）
        if len(aim_line_indexes[0]) < 2 or len(aim_line_indexes[1]) < 2:
            logger.info('未找到足够多的的框线')
            return []

        aim_line_indexes[0] = [min(aim_line_indexes[0]), max(aim_line_indexes[0])]
        aim_line_indexes[1] = [min(aim_line_indexes[1]), max(aim_line_indexes[1])]
        logger.info('找到框线：%s', aim_line_indexes)
        selected_lines = [self.lines[0][aim_line_indexes[0][0]],
                          self.lines[0][aim_line_indexes[0][1]],
                          self.lines[1][aim_line_indexes[1][0]],
                          self.lines[1][aim_line_indexes[1][1]]
                          ]
        self.is_frame_ok = True
        four_points = get_four_intersaction_points(selected_lines)
        self.four_points = four_points

        return four_points

    # 4点透射变换
    def four_point_transform(self, four_points):
        src = np.array(four_points, np.float32)
        # 高和宽成比例
        if self.w/self.h < idcard_w2h_ratio:
            w = self.w
            h = w / idcard_w2h_ratio
        else:
            h = self.h
            w = h * idcard_w2h_ratio
        # 目标图
        dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
        P = cv2.getPerspectiveTransform(src, dst)  # 计算投影矩阵
        w, h = int(w), int(h)
        self.img = cv2.warpPerspective(self.img, P, (w, h), borderValue=125)
        self.h, self.w = self.img.shape[:2]
        logger.info('完成投射变换')

        if DEBUG: cv2.imwrite('debug/3lsd_affine.jpg', self.img)

        return self.img

    def crop_subimg_by_template(self):

        name_img = self.img[int(self.h*0.11):int(self.h*0.24), int(self.w*0.18):int(self.w*0.4)]
        sex_img = self.img[int(self.h * 0.25):int(self.h * 0.35),int(self.w * 0.18):int(self.w * 0.25)]
        nation_img = self.img[int(self.h * 0.24):int(self.h * 0.34),int(self.w * 0.39):int(self.w * 0.44)]
        birthday_img = self.img[int(self.h * 0.35):int(self.h * 0.48), int(self.w * 0.18):int(self.w * 0.61)]
        address_img_1 = self.img[int(self.h * 0.48):int(self.h * 0.58), int(self.w * 0.17):int(self.w * 0.62)]
        address_img_2 = self.img[int(self.h * 0.58):int(self.h * 0.68), int(self.w * 0.17):int(self.w * 0.62)]
        address_img_3 = self.img[int(self.h * 0.68):int(self.h * 0.78), int(self.w * 0.17):int(self.w * 0.62)]
        idcard_img = self.img[int(self.h * 0.8):int(self.h * 0.91), int(self.w * 0.34):int(self.w * 0.93)]
        subimg = [name_img, sex_img, nation_img, birthday_img, address_img_1, address_img_2, address_img_3, idcard_img]
        logger.info('完成切图')

        if DEBUG:
            for i, img in enumerate(subimg):
                cv2.imwrite('debug/'+'5subimg_'+str(i)+'.jpg', img)

        return subimg

    def crop_and_recognize_by_template(self):
        if not self.is_frame_ok:
            logger.info('lsd未检测到框线，无法通过lsd定位身份证区域')
            return False
        self.four_point_transform(self.four_points)
        subimg = self.crop_subimg_by_template()
        final_result = img2string.recognize_subimg(subimg)

        return final_result



