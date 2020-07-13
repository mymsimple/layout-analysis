import sys

import numpy as np
import cv2


def test_detect(img_path):
    # 参考：https://blog.csdn.net/yuanlulu/article/details/90081644
    # 参考：https://blog.csdn.net/it2153534/article/details/79185397
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # 二值化图片
    ret, th = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    kernel = np.ones((10, 20), np.uint8)
    # 开运算
    closing = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    # 腐蚀
    kernel = np.ones((5, 10), np.uint8)
    dilation = cv2.erode(closing, kernel, iterations=1)

    #  查找和筛选文字区域
    region = []
    #  查找轮廓
    img2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 利用以上函数可以得到多个轮廓区域，存在一个列表中。
    #  筛选那些面积小的
    for i in range(len(contours)):
        # 遍历所有轮廓
        # cnt是一个点集
        cnt = contours[i]

        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)

        # 面积小的都筛选掉、这个300可以按照效果自行设置
        if (area < 300):
            continue

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        # 打印出各个矩形四个点的位置
        # print("rect is: ")
        # print(rect)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        if (height > width):
            continue

        region.append(box)

    color = cv2.cvtColor(dilation, cv2.COLOR_GRAY2RGB)
    h,w,_ = color.shape
    print(color.shape)

    for box in region:
        cv2.drawContours(color, [box], 0, (0, 0, 255), 2)

    #cv2.imshow('gray', color)
    #cv2.imwrite("test/4_gray.jpg",color)
    #cv2.waitKey(0)  # 无限期等待输入

    box_point = convert(region,w)
    return box_point,img



def convert(region,w):
    box_point = []
    for box in region:
        x = []
        x.append(box[0][0])
        x.append(box[1][0])
        x.append(box[2][0])
        x.append(box[3][0])
        y = []
        y.append(box[0][1])
        y.append(box[1][1])
        y.append(box[2][1])
        y.append(box[3][1])

        x_max = max(x)
        x_min = min(x)
        y_max = max(y)
        y_min = min(y)

        if x_min == 0 or y_min == 0 or x_max - x_min >= w/2: continue
        else:
            pos = {}
            pos['x'] = x_min
            pos['y'] = y_min
            pos['w'] = x_max - x_min
            pos['h'] = y_max - y_min
            box_point.append(pos)

    return box_point



if __name__ == '__main__':
    test_detect('data/4.jpg')
