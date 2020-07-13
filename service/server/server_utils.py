#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
import tensorflow as tf
import sys
from collections import namedtuple
from server import conf
from server.conf import system_config
from vo.cfg.system_config import ModelParamConfig
from service.model_call import model_utils, model_call_service


logger = logging.getLogger(__name__)

'''
@Title   : server 模块相关服务
@File    :   server_utils.py    
@Author  : vin
@Time    : 2020/5/20 6:00 下午
@Version : 1.0 
'''


def restore_model(model_param: ModelParamConfig):
    input_map = {}
    output_map = {}
    for v in model_param.input:
        input_map[v.name] = v.name
    for v in model_param.output:
        output_map[v.name] = v.name
    # 统一不在使用别名了
    model_param.model_params = model_utils.restore_model_by_dir(model_param.model_path,
                                                                input_map,
                                                                output_map)


def init_single(mode):
    logger.info("启动加载模型模式")
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3, allow_growth=True)
    config = tf.ConfigProto(gpu_options=gpu_options)
    config.allow_soft_placement = True
    logger.debug("开始初始化各模型参数")
    if mode == conf.MODE_SINGLE:
        # 模型加载
        restore_model(system_config.table_detect_params)

    logger.info("参数初始化结束！")


def get_version():
    version_file = "../version.txt"

    import os
    if not os.path.exists(version_file):
        return "测试版"

    with open(version_file) as f:
        version = f.read()
        return version
