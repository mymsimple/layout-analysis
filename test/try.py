# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

# arr = np.random.randint(1, 10, size=[1, 5, 5])
# print("arr:",arr)
# mask = arr<5
# arr[mask] = 0 # 把标记为True的值记为0
# print("arr:",arr)

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


def test2():
    imgfile = 'data/test/1.jpg'
    pngfile = 'data/test/1.png'

    img = cv2.imread(imgfile, 1)
    mask = cv2.imread(pngfile, 0)
    cv2.imwrite("data/test/11.png",mask)

    contours, _, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("contours:",contours)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

    img = img[:, :, ::-1]
    img[..., 2] = np.where(mask == 1, 255, img[..., 2])
    show(img)



def test3():
    img = cv2.imread('data/test/test1.jpg')
    #img = cv2.imread('data/test/2.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #show(gray)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #show(binary)

    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(type(contours))
    #print(type(contours[0]))
    print(len(contours))

    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    #show(img)
    #cv2.imwrite("data/test/test1_1.jpg",img)



    # # 显示轮廓，tmp为黑色的背景图
    # tmp = np.zeros(img.shape, np.uint8)
    # res = cv2.drawContours(tmp, contours, -1, (250, 255, 255), 1)
    # show(res)
    #
    # 外接图形
    cnt = contours[1]
    # x, y, w, h = cv2.boundingRect(cnt)
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 3)
    # #cv2.imwrite("data/test/jx1_1.jpg", img)
    # show(img)

    # 旋转矩形
    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    # cv2.imwrite("data/test/xzjx1_1.jpg", img)


    # 极值
    pentagram = contours[1] # 第二条轮廓是五角星  

    leftmost = tuple(pentagram[:, 0][pentagram[:, :, 0].argmin()])
    rightmost = tuple(pentagram[:, 0][pentagram[:, :, 0].argmax()])
    upmost = tuple(pentagram[:, 0][pentagram[:, :, 1].argmin()])
    downmost = tuple(pentagram[:, 0][pentagram[:, :, 1].argmax()])


    cv2.circle(img, leftmost, 2, (0, 0, 255), 5)
    cv2.circle(img, rightmost, 2, (0, 0, 255), 5)
    cv2.circle(img, upmost, 2, (0, 0, 255), 5)
    cv2.circle(img, downmost, 2, (0, 0, 255), 5)

    #cv2.imwrite("data/test/jzd1_1.jpg", img)
    show(img)



def test4():
    img = cv2.imread("data/test/1.jpg")
    mask = cv2.imread('data/test/1.png', cv2.IMREAD_GRAYSCALE)  # 将彩色mask以二值图像形式读取
    masked = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask)  # 将image的相素值和mask像素值相加得到结果
    cv2.imwrite('data/test/1_masked.jpg', masked)



def test5():
    import numpy as np
    a = np.array([[[True, False],[True, False],[True, False]],
                  [[True, False],[True, False],[True, False]],
                  [[True, False],[True, False],[True, False]]])
    print(a)
    print(a + 0)
    print(a * 255)


def test6():
    arr = np.random.randint(1, 10, size=[1, 5, 5])
    print("arr:",arr)
    mask = arr<5
    arr[mask] = 0 # 把标记为True的值记为0
    print("arr:",arr)


def point_judge(center, bbox):
    """
    用于将矩形框的边界按顺序排列
    :param center: 矩形中心的坐标[x, y]
    :param bbox: 矩形顶点坐标[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    :return: 矩形顶点坐标,依次是 左下, 右下, 左上, 右上
    """
    left = []
    right = []
    for i in range(4):
        if bbox[i][0] > center[0]:  # 只要是x坐标比中心点坐标大,一定是右边
            right.append(bbox[i])
        else:
            left.append(bbox[i])
    if right[0][1] > right[1][1]:  # 如果y点坐标大,则是右上
        right_down = right[1]
        right_up = right[0]
    else:
        right_down = right[0]
        right_up = right[1]

    if left[0][1] > left[1][1]:  # 如果y点坐标大,则是左上
        left_down = left[1]
        left_up = left[0]
    else:
        left_down = left[0]
        left_up = left[1]
    return left_down, right_down, left_up, right_up



def test7():
    # 此方法没跑通，被否定
    # img = cv2.imread("data/idcard/input/28.jpg",0)
    # print(img.shape)
    img = cv2.imread("data/idcard/input/28.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img_gray)

    ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 寻找二值化图中的轮廓
    image, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))  # 结果应该为2

    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # 按照面积大小排序

    countours_res = []
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])  # 计算面积

        if (area <= 0.4 * img.shape[0] * img.shape[1]) and (area >= 0.05 * img.shape[0] * img.shape[1]):
            # 人为设定,身份证正反面框的大小不会超过整张图片大小的0.4,不会小于0.05(这个参数随便设置的)
            rect = cv2.minAreaRect(contours[i])  # 最小外接矩,返回值有中心点坐标,矩形宽高,倾斜角度三个参数
            box = cv2.boxPoints(rect)
            left_down, right_down, left_up, right_up = point_judge([int(rect[0][0]), int(rect[0][1])], box)
            src = np.float32([left_down, right_down, left_up, right_up])  # 这里注意必须对应

            dst = np.float32([[0, 0], [int(max(rect[1][0], rect[1][1])), 0], [0, int(min(rect[1][0], rect[1][1]))],
                              [int(max(rect[1][0], rect[1][1])),
                               int(min(rect[1][0], rect[1][1]))]])  # rect中的宽高不清楚是个怎么机制,但是对于身份证,肯定是宽大于高,因此加个判定
            m = cv2.getPerspectiveTransform(src, dst)  # 得到投影变换矩阵
            result = cv2.warpPerspective(img, m, (int(max(rect[1][0], rect[1][1])), int(min(rect[1][0], rect[1][1]))),
                                         flags=cv2.INTER_CUBIC)  # 投影变换
            countours_res.append(result)
    return countours_res  # 返回身份证区域




def convert():
    '''
    binary ===> img
    '''
    binary = [[0],
              [1],
              [2],
              [3]]

    binary = np.array(binary)
    #print("binary:",binary)

    # img = [[0 0 0 0]
    #       [0 0 0 0]]


    binary.reshape(1,-1)
    #print(binary)


z = np.array([[[1],
              [2],
              [3],
              [4]],
              [[1],
              [2],
              [3],
              [4]]])
z = z.reshape(len(z),-1)
print(type(z))
print("z:",z)





if __name__ == "__main__":
    # countours_res = test7()
    # cv2.imwrite("./data/idcard/28.jpg", np.array(countours_res))
    # print(countours_res)

    convert()
