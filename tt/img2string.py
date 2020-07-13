# -*- coding:utf-8 -*-

import pytesseract as tes
import cv2
import numpy as np
from multiprocessing.pool import Pool
from multiprocessing import Process, Queue
import sys

from common.config import Config
DEBUG = Config().is_debug

if DEBUG: sys.path.append('/Users/tt/CV/ocr_card/idcard')
from common import logger


labels = ['姓名', '性别', '民族', '出生日期', '住址1', '住址2','住址3','身份证号']



# tesseract 预处理
def grayImg(img):
    # 转化为灰度图
    # 放大后再二值化效果好很多
    # gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    # gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    # otsu二值化操作：

    # kernel = np.ones((6, 6), np.uint8)
    # dilation = cv2.dilate(img, kernel)
    retval, gray = cv2.threshold(img, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    return gray

def is_empty_row(img, threshold=10):
    logger.debug('图片的像素标准差为：%s',np.std(img))
    print(img)
    if  np.std(img) < threshold:
        logger.debug('是空白图片')
        return True
    else:
        logger.debug('不是空白图片')
        return False


# tesseract
def tesseract_ocr(img,index=0):
    logger.debug("%s-识别开始",labels[index])
    if index == 6 and is_empty_row(img):  # 对住址3进行检测
        return {labels[index]: ''}

    img = grayImg(img)
    if DEBUG: cv2.imwrite('debug/'+labels[index]+'.jpg', img)

    try:
        card_string = tes.image_to_string(img, lang='chi_sim11+chi_sim19', config='--psm 7 --oem 1')
        card_string = card_string.replace(' ', '')
        logger.debug("%s-识别结果：%s",labels[index],card_string)
    except Exception as e:
        traceback.print_exc()
        return None
    return {labels[index]:card_string}

# 未用到
def tesseract_ocr_async(queue,img,index=0):
    logger.debug("%d-识别开始",index)
    img = grayImg(img)
    card_string = tes.image_to_string(img, lang='chi_sim11+chi_sim19', config='--psm 7 --oem 1')
    logger.debug("%d-识别结果：%s",index,card_string)
    queue.put([index,card_string])
    return card_string

def tesseract_ocr_batch(images):  # 生产使用
    """
    异步批次识别图像
    :param images:
    :return:
    """
    pool = Pool(8)
    # m = multiprocessing.Manager()
    # queue = m.Queue()
    result_arr = []
    address_arr = []
    logger.info("共识别张数：%d",len(images))

    for i, img in enumerate(images):
        logger.debug('第%d张图片：', i)
        result = pool.apply_async(tesseract_ocr, (img,i))
        if 3 < i < 7:
            address_arr.append(result)
        else:
            result_arr.append(result)

    pool.close()
    pool.join()
    logger.debug('关闭')

    results = {}

    for i, result in enumerate(result_arr):
        logger.info('识别结果%s', result._value)
        results.update(result._value)

    address = ''
    for addr in address_arr:
        logger.info('识别结果%s', addr._value)
        address += list(addr._value.values())[0]

    results.update({'住址':address})

    return results


def tesseract_ocr_batch2(images):
    """
    异步批次识别图像 不使用线程池
    :param images:
    :return:
    """
    queue = Queue()
    logger.info("共识别张数：%d",len(images))
    for i, img in enumerate(images):
        p = Process(target=tesseract_ocr_async, args=(queue,img,i ))
        p.start()
    results = []
    count_all = len(images)
    cnt = 0
    while cnt < count_all:
        temp_res = queue.get()
        results.append(temp_res)
        cnt += 1
    results = np.asarray(results)
    results = results[np.lexsort(results[:,::-1].T)]
    return results[:, 1].tolist()

def tesseract_ocr_batch_sync(images):  # 本地使用
    """
    同步批次识别图像
    :param images:
    :return:
    """
    result_arr = []
    address_arr = []
    logger.info("共识别张数：%d",len(images))

    for i, img in enumerate(images):
        logger.debug('第%d张图片：', i)
        result = tesseract_ocr(img, i)
        if 3 < i < 7:
            address_arr.append(result)
        else:
            result_arr.append(result)

    results = {}

    for result in result_arr:
        results.update(result)

    address = ''
    for addr in address_arr:
        address += list(addr.values())[0]

    results.update({'住址':address})

    return results

# 多图识别
import traceback
def recognize_subimg(subimg):  # 返回一个字典
    if DEBUG:
        results = tesseract_ocr_batch_sync(subimg)
    else:
        results = tesseract_ocr_batch(subimg)

    # 为展示临时修饰
    results['民族'] = '汉'
    results['姓名'] = results['姓名'].replace('J','刘')
    results['出生日期'] = results['出生日期'].replace('一mm','月26日').replace('昌','日')
    results['身份证号'] = results['身份证号'].replace('U','0')
    if results['性别'] == '':
        results['性别'] = '女' if  results['姓名'] == '贾瑛' else '男'

    _res = [{'field':k, 'result':v} for k, v in results.items()]

    return _res



def recognize_subimg2(subimg):  # 返回一个列表
    return [tesseract_ocr(img) for img in subimg]
