# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import base64
import numpy as np
import os
import matplotlib
import cv2
import re
import pandas as pd
import time
from tqdm import tqdm
from card.ID_template import crnn
import logging
from card import cfg
CFG = cfg.CFG



'''
    调用local系统OCR相关接口(psenet+crnn)
'''

matplotlib.use('TkAgg')
logger = logging.getLogger("身份证图片识别-local(psenet+crnn)")

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])


def ocr_psenet(img_base64):
    url = CFG['local']['url'] + "detect/detect.ajax"
    post_data = {"img": img_base64,
                 "sid": "iamsid",
                 "do_verbose": False,
                 'detect_model': 'ctpn'
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=post_data, headers=headers)
    data = response.json()
    logger.info("返回报文格式:%s",data)
    return data


def points_to_img(data,image):
    images = []
    boxes = data['detect_info']
    pts_all = []
    for box in boxes:
        x = []
        y = []
        for point in box:
            x.append(point['x'])
            y.append(point['y'])

        x_max = max(x)
        y_max = max(y)
        x_min = min(x)
        y_min = min(y)
        w = x_max - x_min
        h = y_max - y_min
        img = image[y_min:y_min+h,x_min:x_min+w]
        cv2.imwrite("data/cut/test11.jpg", img)
        pts = {
            'x': x_min,
            'y': y_min,
            'w': w,
            'h': h
        }
        images.append(img)
        pts_all.append(pts)
    return images, pts_all


def result_reconstruct(images,boxes):
    result = crnn(images)
    results = []
    for i in range(len(boxes)):
        pos = boxes[i]
        img = images[i]
        cv2.imwrite('data/small_images/' + str(i) + '.jpg', img)
        txt = result['prism_wordsInfo'][i]['word']
        if txt is None or txt.strip() == "": continue
        one_image_info = {
            'pos': pos,
            'txt': txt
        }
        results.append(one_image_info)
    logger.info("切图进crnn识别后的结果：%s", results)
    return results,result


'''
[{'pos': {'x': 319, 'y': 119, 'w': 220, 'h': 91}, 'txt': '刘浩越'}, 
 {'pos': {'x': 118, 'y': 276, 'w': 75, 'h': 59}, 'txt': '性'}, 
 {'pos': {'x': 205, 'y': 282, 'w': 58, 'h': 53}, 'txt': '别'}, 
 {'pos': {'x': 319, 'y': 276, 'w': 58, 'h': 70}, 'txt': '男'}, 
 {'pos': {'x': 486, 'y': 282, 'w': 58, 'h': 58}, 'txt': '闲'}, 
 {'pos': {'x': 578, 'y': 282, 'w': 47, 'h': 53}, 'txt': '族'}, 
 {'pos': {'x': 648, 'y': 282, 'w': 53, 'h': 58}, 'txt': '汉'}, 
 {'pos': {'x': 648, 'y': 407, 'w': 69, 'h': 64}, 'txt': '月'}, 
 {'pos': {'x': 135, 'y': 418, 'w': 42, 'h': 47}, 'txt': 'N'}, 
 {'pos': {'x': 319, 'y': 412, 'w': 139, 'h': 59}, 'txt': '2006'}, 
 {'pos': {'x': 475, 'y': 412, 'w': 69, 'h': 53}, 'txt': '销'}, 
 {'pos': {'x': 578, 'y': 412, 'w': 31, 'h': 53}, 'txt': '1'}, 
 {'pos': {'x': 708, 'y': 407, 'w': 145, 'h': 64}, 'txt': '168'}, 
 {'pos': {'x': 210, 'y': 543, 'w': 53, 'h': 63}, 'txt': '斌'}, 
 {'pos': {'x': 297, 'y': 543, 'w': 680, 'h': 74}, 'txt': '北京市朝阳区水礁子北里'}, 
 {'pos': {'x': 313, 'y': 635, 'w': 329, 'h': 74}, 'txt': '8楼东701号'}, 
 {'pos': {'x': 129, 'y': 890, 'w': 123, 'h': 69}, 'txt': '公民'}, 
 {'pos': {'x': 254, 'y': 890, 'w': 247, 'h': 69}, 'txt': '身份号码'}, 
 {'pos': {'x': 584, 'y': 885, 'w': 874, 'h': 80}, 'txt': '110105200601164510'}, 
 {'pos': {'x': 259, 'y': 895, 'w': 10, 'h': 32}, 'txt': '1'}]
'''


def get_gap(res):
    '''
    找到行间距
    '''
    for r in res:
        for k in list(r.keys()):
            if not r[k]:
                del r[k]

    def cmpx(elem):
        return elem['pos']['x']

    res.sort(key=cmpx)
    # res_top = res[:10]
    res_top = res

    def cmpy(elem):
        return elem['pos']['y']
    res_top.sort(key=cmpy)

    res_top = res_top[0:2]
    # print("1:", res_top[0]['txt'])
    # print("2:", res_top[1]['txt'])
    # print("res_top[0]['pos']['y']:", res_top[0]['pos']['y'])
    # print("res_top[1]['pos']['y']:", res_top[1]['pos']['y'])

    GAP = abs(res_top[0]['pos']['y'] - res_top[1]['pos']['y'])
    current_max_y = min(res_top[0]['pos']['y'], res_top[1]['pos']['y'])

    for r in res_top:
        txt = r['txt']
        if txt.find('名') == 1 or txt.find('姓') == 1:
            y1 = r['pos']['y']
            if txt.find('性') == 1 or txt.find('别') == 1:
                y2 = r['pos']['y']
                GAP = y2 -y1
                current_max_y = y1

    logger.info("前两行y坐标差:%s", GAP)

    return res, GAP, current_max_y


def split_line(res, GAP, current_max_y):
    '''
    按行分组
    '''
    def cmpy(elem):
        return elem['pos']['y']
    res.sort(key=cmpy)

    row = 0
    for r in res:
        y = r['pos']['y']
        if abs(y - current_max_y) > GAP/2:
            row += 1
            current_max_y = y
            r['row'] = row
        else:
            r['row'] = row

    # 先按行-'row'进行分组
    x = [r['pos']['x'] for r in res]
    row = [r['row'] for r in res]
    txt = [r['txt'] for r in res]
    result = pd.DataFrame({'x':x,'row':row,'txt':txt})
    logger.debug("按行分组后的结果：%s",result)

    return result


def analysis(result):
    '''
    按行遍历，同行字符串拼接，然后拿"姓名/性别......"等关键字查找并删除匹配上的字符串，剩余的按行输出就是我们要的结果
    :param result:
    :return:
    '''
    result_grouped = result.groupby('row')
    result_dict = {1:['姓名:','[姓,名]'],2:['性别民族:','[性,别,民,族]'],
                  3:['出生:','[出,生,年,月,日]'],4:['住址:','[住,址]'],5:['住址:','[住,址]'],
                  6:['公民身份号码:','[公,民,身,份,号,码]']}

    logger.info("-------------------身份证解析--------------------")
    i = 0
    for row, group in result_grouped:
        group_sort = group.sort_values(by='x')
        str = list(group_sort['txt'])
        info = ''.join(str)
        i += 1
        output = re.sub(result_dict[i][1], "", info)
        #print("output:",output)

        if i != 4:
            if i == 2:
                if output.find("女") == 1:
                    print("性别:", "女")
                    print("民族:", output[-1])
                else:
                    print("性别:", "男")
                    print("民族:", output[-1])
            elif i == 5:
                zz = re.sub(result_dict[4][1], "", info)
                output = zz + output
                print("住址:", output)
            else:
                print(result_dict[i][0], output)




def convert_idcard(data,image):
    pts_all = []
    for d in data['detect_info']:
        pts = []
        for i in d:
            x = i['x']
            y = i['y']
            pts.append((x,y))
        cv2.polylines(image, np.int32([pts]), color=(0, 0, 255), thickness=3, isClosed=True)
        cv2.imwrite("data/cut/ctpn_9.jpg", image)

    return pts_all


def nparray2base64(img_data):
    """
        nparray格式的图片转为base64（cv2直接读出来的就是）
    :param img_data:
    :return:
    """
    _, d = cv2.imencode('.jpg', img_data)
    return str(base64.b64encode(d), 'utf-8')


if __name__ == '__main__':
    init_logger()

    image = cv2.imread("data/data_test/cut/2BCAFB4E-2FD8-CD58-35F2-3B8C4DEB5665B1-1.jpg")
    #image = cv2.imread("data/data_test/correct/9.jpg")

    img_base64 = nparray2base64(image)
    data = ocr_psenet(img_base64)
    images,boxes = points_to_img(data,image)
    #result = crnn(images)
    results, result = result_reconstruct(images, boxes)
    res, GAP, current_max_y = get_gap(results)
    result = split_line(res, GAP, current_max_y)
    analysis(result)

    #画框测试
    #convert_idcard(data,image)





'''
local psenet api 返回的报文格式：
data: { 'code': '0', 
        'detect_info': [[{'x': 1255, 'y': 1617}, {'x': 889, 'y': 1448}, {'x': 953, 'y': 1305}, {'x': 1319, 'y': 1474}], 
                        [{'x': 500, 'y': 1523}, {'x': 500, 'y': 1435}, {'x': 586, 'y': 1435}, {'x': 586, 'y': 1523}], 
                        [{'x': 641, 'y': 1576}, {'x': 641, 'y': 1488}, {'x': 727, 'y': 1488}, {'x': 727, 'y': 1576}], 
                        [{'x': 820, 'y': 1667}, {'x': 820, 'y': 1566}, {'x': 920, 'y': 1566}, {'x': 920, 'y': 1667}], 
                        [{'x': 384, 'y': 1745}, {'x': 384, 'y': 1631}, {'x': 509, 'y': 1631}, {'x': 509, 'y': 1745}], 
                        [{'x': 564, 'y': 1784}, {'x': 564, 'y': 1696}, {'x': 625, 'y': 1696}, {'x': 625, 'y': 1784}], 
                        [{'x': 1202, 'y': 1798}, {'x': 1116, 'y': 1798}, {'x': 1116, 'y': 1696}, {'x': 1202, 'y': 1696}], 
                        [{'x': 1231, 'y': 1863}, {'x': 1231, 'y': 1762}, {'x': 1356, 'y': 1762}, {'x': 1356, 'y': 1863}], 
                        [{'x': 960, 'y': 1951}, {'x': 708, 'y': 1894}, {'x': 736, 'y': 1764}, {'x': 989, 'y': 1821}], 
                        [{'x': 1334, 'y': 1928}, {'x': 1334, 'y': 1801}, {'x': 1459, 'y': 1801}, {'x': 1459, 'y': 1928}], 
                        [{'x': 320, 'y': 1941}, {'x': 320, 'y': 1853}, {'x': 394, 'y': 1853}, {'x': 394, 'y': 1941}]], 
        'message': 'success', 
        'sid': 'iamsid'}
'''