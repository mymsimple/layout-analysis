import matplotlib
import cv2
import numpy as np
import logging

'''
    这种方法是膨胀，找轮廓，最大的四边形就是！
'''

matplotlib.use('TkAgg')
logger = logging.getLogger("身份证图片识别")

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

def filter_gaussian(img):
    # 原来内核大小只支持奇数
    blur = cv2.GaussianBlur(img, (5,5), 0)  # （5,5）表示的是卷积模板的大小，0表示的是沿x与y方向上的标准差
    logger.info("高斯模糊")
    return blur

def detect(img):
    #1. 高斯模糊
    blur = filter_gaussian(img)
    cv2.imwrite("photo/blur.jpg", blur)
    logger.info("已生成模糊图【%s】", "photo/blur.jpg")

    #2. 转化成灰度图
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("photo/gray.jpg", gray)
    logger.info("已生成灰度图【%s】", "photo/gray.jpg")

    # # 3. 自适应二值化方法
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 2)
    _,binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imwrite("photo/binary.jpg", binary)
    logger.info("已生成二值化图【%s】", "photo/binary.jpg")

    # 膨胀
    kernel = np.ones((15,15), np.uint8)
    dilation = cv2.dilate(binary, kernel)
    cv2.imwrite("photo/dilation.jpg", dilation)
    logger.info("已生成膨胀【%s】", "photo/dilation.jpg")

    # 函数cv2.findContours()三个参数：
    #   第一个是输入图像，第二个是轮廓检索模式，第三个是轮廓近似方法。
    # 返回值有三个：
    #   第一个是图像，第二个是轮廓，第三个是（轮廓的）层析结构。
    #   轮廓（第二个返回值）是一个Python列表，其中储存这图像中所有轮廓。
    #   每一个轮廓都是一个Numpy数组，包含对象边界点（x，y）的坐标。
    cnts_img,cnts,_ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite("photo/contours.jpg", cnts_img)
    logger.info("已生成轮廓图【%s】", "photo/contours.jpg")

    docCnt = None
    # 确保至少有一个轮廓被找到
    if len(cnts) == 0: return None
    # 将轮廓按大小降序排序
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # 对排序后的轮廓循环处理
    poly_img = img.copy()
    box_point = []
    for c in cnts:
        logger.debug("轮廓中的点%d个",len(c))
        # 获取近似的轮廓
        peri = cv2.arcLength(c, True)

        # opencv中对指定的点集进行多边形逼近的函数
        # arg1:输入的点集 arg2:指定的精度,也即是原始曲线与近似曲线之间的最大距离  arg3:若为true，则说明近似曲线是闭合的；反之，若为false，则断开
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        logger.debug("由此轮廓围成的多边形%d条边",len(approx))

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        x = []
        x.append(box[0][0])
        x.append(box[1][0])
        x.append(box[2][0])
        x.append(box[3][0])
        y=[]
        y.append(box[0][1])
        y.append(box[1][1])
        y.append(box[2][1])
        y.append(box[3][1])

        x_max = max(x)
        x_min = min(x)
        y_max = max(y)
        y_min = min(y)

        pos = {}
        pos['x'] = x_min
        pos['y'] = y_min
        pos['w'] = x_max - x_min
        pos['h'] = y_max - y_min
        box_point.append(pos)

        cv2.drawContours(poly_img, [box], 0, (255, 0, 0), 3) # 矩形框
        cv2.polylines(poly_img, [approx], True, (0, 0, 255), 2) # 轮廓

    cv2.imwrite("photo/poly.jpg", poly_img)
    logger.info("已生成轮廓多边形图【%s】", "photo/poly.jpg")
    return box_point,gray

# 4点透射变换
def four_point_transform(image, docCnt):
    # 原图
    src = np.array([[docCnt[0][0],docCnt[0][1]],[docCnt[3][0],docCnt[3][1]],[docCnt[1][0],docCnt[1][1]],[docCnt[2][0],docCnt[2][1]]],np.float32)
    # 高和宽
    h,w = image.shape[:2]
    # 目标图
    dst = np.array([[0,0],[w,0],[0,h],[w,h]],np.float32)
    P = cv2.getPerspectiveTransform(src, dst)  # 计算投影矩阵
    r = cv2.warpPerspective(img, P, (w, h), borderValue=125)
    return r

# 根据坐标和备注生成wordinfo对象
def getInfo(x,y,w,h,text):
    word_info = {}
    word_info['word'] = text
    pos = []
    pos1 = {}
    pos1['x'] = x
    pos1['y'] = y
    pos2 = {}
    pos2['x'] = x + w
    pos2['y'] = y
    pos3 = {}
    pos3['x'] = x + w
    pos3['y'] = y + h
    pos4 = {}
    pos4['x'] = x
    pos4['y'] = y + h
    pos.append(pos1)
    pos.append(pos2)
    pos.append(pos3)
    pos.append(pos4)
    word_info['pos'] = pos
    return word_info

def gjj_start(img):
    wordInfo = detect(img)
    return wordInfo

if __name__ == '__main__':
    init_logger()
    import sys

    img = cv2.imread(sys.argv[1])
    wordInfo = detect(img)
    logger.info("识别完成")