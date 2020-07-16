# -*- coding:utf-8 -*-
import logging
import cv2
import os
import requests
import base64
import json
import numpy as np
from utils.cut_and_correct import crop_img
from card import cfg
CFG = cfg.CFG

logger = logging.getLogger("身份证图片识别-模板匹配")

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

key_pos={
    '姓': [[45, 60], [65, 75]],
    '名': [[80, 60], [95, 75]],
    '性': [[45, 107], [63, 123]],
    '别': [[78, 109], [96, 126]],
    '族': [[222, 109], [238, 126]],
    '出': [[46, 156], [62, 173]],
    '生': [[78, 158], [95, 174]],
    '年': [[189, 157], [204, 173]],
    '住': [[45, 210], [65, 225]],
    '址': [[79, 208], [96, 225]],
    '公': [[47, 335], [68, 360]],
    '民': [[70, 335], [87, 360]],
    '身': [[89, 335], [112, 360]],
    '份': [[111, 335], [135, 360]],
    '号': [[152, 335], [172, 360]],
    '码': [[170, 335], [200, 360]]
}


class LsdLiner(object):
    def __init__(self, img):
        self.img = img
        self.h, self.w = img.shape[:2]

    def crop_subimg_by_template(self):
        name_img = self.img[int(self.h * 0.09):int(self.h * 0.24), int(self.w * 0.15):int(self.w * 0.4)]
        sex_img = self.img[int(self.h * 0.23):int(self.h * 0.35), int(self.w * 0.15):int(self.w * 0.25)]
        nation_img = self.img[int(self.h * 0.24):int(self.h * 0.34), int(self.w * 0.35):int(self.w * 0.50)]
        birthday_img = self.img[int(self.h * 0.35):int(self.h * 0.48), int(self.w * 0.16):int(self.w * 0.61)]
        address_img_1 = self.img[int(self.h * 0.48):int(self.h * 0.60), int(self.w * 0.15):int(self.w * 0.62)]
        address_img_2 = self.img[int(self.h * 0.58):int(self.h * 0.70), int(self.w * 0.15):int(self.w * 0.62)]
        address_img_3 = self.img[int(self.h * 0.68):int(self.h * 0.80), int(self.w * 0.15):int(self.w * 0.62)]
        idcard_img = self.img[int(self.h * 0.8):int(self.h * 0.93), int(self.w * 0.31):int(self.w * 0.93)]
        subimg = [name_img, sex_img, nation_img, birthday_img, address_img_1, address_img_2, address_img_3, idcard_img]
        logger.info('套模板完成切图')

        for i, img in enumerate(subimg):
            cv2.imwrite('data/idcard/debug/' + '5subimg_' + str(i) + '.jpg', img)

        return subimg


def nparray2base64(img_data):
    """
        nparray格式的图片转为base64（cv2直接读出来的就是）
    :param img_data:
    :return:
    """
    _, d = cv2.imencode('.jpg', img_data)
    return str(base64.b64encode(d), 'utf-8')


def crnn(images, url='default_url'):
    """
     多张图片的crnn
    :param images_base64:
    :param url:crnn的地址，可以动态传入，以测试不同版本的crnn
    :return:
    """
    if url == 'default_url':
        url = CFG['local']['url'] + "crnn" #"v2/crnn.ajax"

    post_data = []
    for _img in images:
        base64_images = nparray2base64(_img)
        post_data.append({"img": base64_images})

    headers = {'Content-Type': 'application/json'}
    logger.info("请求crnn:%s, image size=%d", url, len(post_data))
    response = requests.post(url, json=post_data, headers=headers)
    logger.info("请求结果:%s", response.status_code)
    if response.content:
        result = response.json()
        logger.debug("crnn返回结果：%s", result)

    return result


# 多图识别
def recognize_img(subimg):  # 返回一个字典
    results = crnn(subimg)
    _res = [{'field':k, 'result':v} for k, v in results.items()]

    return _res


def template_match(warped):
    lsdLiner = LsdLiner(warped[0])
    subimg = lsdLiner.crop_subimg_by_template()
    result = recognize_img(subimg)
    logger.info("******crnn返回结果:%s",result)
    final_result = analysis(result)

    return final_result,subimg


def analysis(result):
    res = result[1]['result']
    results = {
        "姓名": res[0]['word'],
        "性别": res[1]['word'].replace("民","").replace("族",""),
        "民族": res[2]['word'],
        "出生": res[3]['word'],
        "住址": res[4]['word'] + res[5]['word'] + res[6]['word'],
        "公民身份证号": res[7]['word']
    }

    return results


def main(frame_path, images_path, result_path):
    files = os.listdir(frame_path)
    results = []
    for file in files:
        logger.debug("处理文件:%s", file)
        name, _ = os.path.splitext(file)
        img_path = os.path.join(images_path + name + ".jpg")
        image = cv2.imread(img_path)
        if image is None:
            continue
        else:
            json_path = os.path.join(frame_path + file)
            f = open(json_path, "r", encoding='utf-8')
            points = json.load(f)
            points = np.array(points)
            warped = crop_img(image, points)
            final_result = template_match(warped)

            txt = name + ".jpg" + " " + str(final_result)
            results.append(txt)

            cv2.imwrite(os.path.join(cutimg_path + name + ".jpg"), warped[0])
            with open(os.path.join(result_path + "front_result.txt"), "w", encoding='utf-8') as f:
                for res in results:
                    f.write(str(res) + "\n")

    return final_result





frame_path = "./data/idcard/frame/"
images_path = "./data/idcard/input/"
cutimg_path = "./data/idcard/correct/"
result_path = "./data/idcard/"


if __name__ == "__main__":
    init_logger()

    final_result = main(frame_path, images_path, result_path)
    print(final_result)
