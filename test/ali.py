# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import base64
import cv2
import os
import numpy as np
import json

'''
    调用阿里身份证识别接口
'''
'''
返回的报文格式：
{'address': '辽宁省东港市龙王庙镇三道洼村袁家店组080081', 
 'birth': '19861126', 
 'card_region': [{'x': 565, 'y': 407}, {'x': 1131, 'y': 459}, {'x': 1099, 'y': 796}, {'x': 534, 'y': 743}], 
 'config_str': '{"side":"face"}', 
 'face_rect': {'angle': -84.59748840332031, 'center': {'x': 998.728515625, 'y': 587.2501831054688}, 'size': {'height': 94.7061538696289, 'width': 107.4455337524414}}, 
 'face_rect_vertices': [{'x': 956, 'y': 529}, {'x': 1050, 'y': 538}, {'x': 1040, 'y': 645}, {'x': 946, 'y': 636}], 
 'name': '马丽', 
 'nationality': '汉', 
 'num': '110105197611260050', 
 'request_id': '20200618103830_62286c9bac042c95a6d3315adb275861', 
 'sex': '女', 
 'success': True}
'''

appcode = '6d915c16b0284a31befdabdc8f7f256f'

def idcard_ocr(img):
    url = "https://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json"
    #post_data = "{\"image\":\""+img+"\",\"configure\":{\"side\":\"face\"}}"
    post_data = {"image":img,"configure":{"side":"face"}}
    headers = {'Authorization':'APPCODE '+appcode, 'content-type':'application/json; charset=UTF-8'}
    response = requests.post(url, headers=headers, json=post_data)
    #print(response)
    data = response.json()
    print(data)
    return data


def convert_idcard(data):
    pts = []
    for i in data['card_region']:
        x = i['x']
        y = i['y']
        pts.append((x,y))
    return pts


def cv2_to_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return str(base64_str,"utf-8")



if __name__ == "__main__":

    dir = "idcard/images/"
    for file in os.listdir(dir):
        path = os.path.join(dir,file)
        img = cv2.imread(path)
        img_base64 = cv2_to_base64(img)
        data = idcard_ocr(img_base64)
        pts = convert_idcard(data)

        cv2.polylines(img, np.int32([pts]), color=(0, 255, 255), thickness=3, isClosed=True)
        cv2.imwrite(os.path.join("idcard/debug/",file), img)




# 测试
# if __name__ == "__main__":
#     img = cv2.imread('idcard/data/2.jpg')
#     img_base64 = cv2_to_base64(img)
#     data = idcard_ocr(img_base64)
#     pts = convert_idcard(data)
#
#     cv2.polylines(img, np.int32([pts]), color=(0, 0, 255), thickness=3, isClosed=True)
#     cv2.imwrite("idcard/debug/test1.jpg", img)