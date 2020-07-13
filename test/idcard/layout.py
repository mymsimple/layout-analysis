'''
1. image --> 2. contours -->3. rectangle, 2 points + theta

4. cut images from the sloped rectangle, after that, images must be a standard rectangle

5.send to crnn api to get below data
[{
    'img':'<BASE64>'
},]

crnn api =====>

[{
    'text':'xxxxx', <----from crnn
    'pos':[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
},]
6. layout analysis, there must be algorithm to syntaxly to figure out the which text correponding to which rectangle.

[{
    'type':'name'
    'text':'xxxxx', <----from crnn
    'pos':[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
},..]

'''

import base64
import cv2
import json
import requests
from counters import detect
import pandas as pd
import re
import matplotlib
import logging
import config
CFG = config.CFG


'''
    传统图像处理算法切图+crnn识别身份证
'''

matplotlib.use('TkAgg')
logger = logging.getLogger("身份证图片识别")

def crnn(images):
    url = CFG['local']['url'] + "crnn"
    base64_images = nparray2base64(images)
    post_data = [{"img":img64} for img64 in base64_images]
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=post_data, headers=headers)
    res = response.text
    data = json.loads(res)
    return data


def nparray2base64(data):
    if type(data) == list:
        result = []
        for d in data:
            base64_data = cv2_to_base64(d)
            imgStr = base64_data.decode()
            result.append(imgStr)
        return result
    return str(base64.b64encode(data), 'utf-8')

def crop_small_images(img, polygens):
    cropped_images = []
    for pts in polygens:
        #print("pts:", pts)
        x = pts['x']
        y = pts['y']
        w = pts['w']
        h = pts['h']
        crop_img = img[y:y+h, x:x+w]
        cropped_images.append(crop_img)
    return cropped_images


'''
切图进crnn识别后的结果result:
([{'pos': {'x': 214, 'y': 106, 'w': 339, 'h': 280}, 'txt': '叉'}, 
  {'pos': {'x': 110, 'y': 236, 'w': 262, 'h': 69}, 'txt': '嵩湖省营夕法尼亚大'}, {'pos': {'x': 48, 'y': 356, 'w': 143, 'h': 32}, 'txt': '公民身份证号码'}, {'pos': {'x': 114, 'y': 108, 'w': 80, 'h': 37}, 'txt': '奥巴马'}, {'pos': {'x': 235, 'y': 148, 'w': 79, 'h': 36}, 'txt': '肯尼亚'}, {'pos': {'x': 45, 'y': 152, 'w': 61, 'h': 32}, 'txt': '性则'}, {'pos': {'x': 47, 'y': 111, 'w': 60, 'h': 32}, 'txt': '姓名'}, {'pos': {'x': 174, 'y': 152, 'w': 59, 'h': 31}, 'txt': '民族'}, {'pos': {'x': 47, 'y': 195, 'w': 58, 'h': 32}, 'txt': '幽生'}, {'pos': {'x': 46, 'y': 243, 'w': 58, 'h': 30}, 'txt': '筐斌'}, {'pos': {'x': 114, 'y': 194, 'w': 54, 'h': 31}, 'txt': '1961'}, {'pos': {'x': 205, 'y': 192, 'w': 51, 'h': 32}, 'txt': '8月'}, {'pos': {'x': 259, 'y': 193, 'w': 50, 'h': 30}, 'txt': '4自'}, {'pos': {'x': 116, 'y': 151, 'w': 33, 'h': 35}, 'txt': '男'}, {'pos': {'x': 173, 'y': 195, 'w': 29, 'h': 30}, 'txt': '年'}, {'pos': {'x': 451, 'y': 293, 'w': 39, 'h': 40}, 'txt': 'A'}, {'pos': {'x': 7, 'y': 181, 'w': 15, 'h': 16}, 'txt': '制'}], array([[140, 140],
       [139, 138]], dtype=uint8))
'''
def analysis(result):
    row = 0
    logger.info("切图进crnn识别后的结果：%s",result)
    for r in result[0]:
        for k in list(r.keys()):
            if not r[k]:
                del r[k]

    def cmpx(elem):
        return elem['pos']['x']
    res = result[0]
    res.sort(key=cmpx)
    res_top = res[:5]

    def cmpy(elem):
        return elem['pos']['y']
    res_top.sort(key=cmpy)
    res_top = res[0:2]
    GAP = abs(res_top[0]['pos']['y']-res_top[1]['pos']['y'])
    current_max_y = min(res_top[0]['pos']['y'], res_top[1]['pos']['y'])
    print(current_max_y)

    res.sort(key=cmpy)

    for r in res:
        y = r['pos']['y']
        if abs(y - current_max_y) > GAP/2:#and y - current_max_y < 4*GAP:
            row += 1
            current_max_y = y
            r['row'] = row
        else:
            r['row'] = row

# 先按行-'row'进行分组
    x = [r['pos']['x'] for r in result[0]]
    row = [r['row'] for r in result[0]]
    txt = [r['txt'] for r in result[0]]
    result = pd.DataFrame({'x':x,'row':row,'txt':txt})

# 按行遍历，同行字符串拼接，然后拿"姓名/性别......"等关键字查找并删除匹配上的字符串，剩余的按行输出就是我们要的结果
    result_grouped = result.groupby('row')
    result_dict = {1:['姓名:','[姓,名]'],2:['性别民族:','[性,别,民,族]'],
                  3:['出生:','[出,生,年,月,日]'],4:['住址:','[住,址]'],
                  5:['公民身份号码:','[公,民,身,份,号,码]']}
    for row,group in result_grouped:
        group_sort = group.sort_values(by='x')
        str = list(group_sort['txt'])
        info = ''.join(str)
        #print('result_dict',result_dict[row][1])
        output = re.sub(result_dict[row][1], "", info)
        print(result_dict[row][0], output)


def cut_contours(image):
    return detect(image)

def cut_and_recognize(image):
    positions,gray = cut_contours(image) # 切图
    small_images = crop_small_images(gray,positions)
    small_text = crnn(small_images)

    result = []
    for i in range(len(positions)):
        pos = positions[i]
        img = small_images[i]
        cv2.imwrite('../debug/' + str(i) + '.jpg',img)
        txt = small_text['prism_wordsInfo'][i]['word']
        if txt is None or txt.strip() == "": continue
        one_image_info = {
            'pos':pos,
            'txt':txt
        }
        result.append(one_image_info)
    return result


def cv2_to_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def main(image_path):
    image = cv2.imread(image_path)
    result = cut_and_recognize(image)
    analysis(result)


if __name__ == "__main__":
    image_path = './idcard/data/2BCAFB4E-2FD8-CD58-35F2-3B8C4DEB5665B1-1.jpg'
    main(image_path)
