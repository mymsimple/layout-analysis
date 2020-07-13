#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    模型相关工具类
    1、 恢复模型
    2、 保存模型
"""

import os
import tensorflow as tf
import logging

logger = logging.getLogger(__name__)


def restore_model_by_dir(model_path, input_map, output_map):
    """
        从目录下寻找最新的模型加载
    :param model_path:
    :param input_map: 变量映射关系 key为模型里存的变量，value为输出params的参数
    :param output_map:
    :return:
    """
    if not os.path.exists(model_path):
        logger.error("Model:[%s] not exist.", model_path)
        return None

    f_list = os.listdir(model_path)
    dirs = [i for i in f_list if os.path.isdir(os.path.join(model_path, i))]
    max_dir = max(dirs)
    return restore_model(os.path.join(model_path, max_dir), input_map, output_map)


def restore(sess, model_path):
    """
        直接指定模型  TODO 这个还有点问题，想训练恢复来着，后来有bug
    :param model_path:
    :return:
    """
    f_list = os.listdir(model_path)
    dirs = [i for i in f_list if os.path.isdir(os.path.join(model_path, i))]
    max_dir = max(dirs)
    real_path = os.path.join(model_path, max_dir)
    print("恢复模型:", real_path)
    tf.get_variable_scope().reuse_variables()
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], real_path)


def restore_model(model_path, input_dict, output_dict):
    """
        直接指定模型
    :param model_path:
    :return:
    """
    logger.info("恢复模型：%r,%r,%r", model_path, input_dict, output_dict)
    # tf.reset_default_graph()
    params = {}
    # g = tf.get_default_graph()
    g = tf.Graph()
    with g.as_default():
        # 从pb模型直接恢复 TODO ! 这里的config也可以从参数里传过来
        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        # init = tf.global_variables_initializer()
        # sess.run(init)

        meta_graph_def = tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], model_path)
        signature = meta_graph_def.signature_def
        if input_dict:
            for input_k in input_dict:
                in_tensor_name = signature['serving_default'].inputs[input_k].name
                input_param = sess.graph.get_tensor_by_name(in_tensor_name)
                params[input_dict[input_k]] = input_param
        if output_dict:
            for output_k in output_dict:
                out_tensor_name = signature['serving_default'].outputs[output_k].name
                output_param = sess.graph.get_tensor_by_name(out_tensor_name)
                params[output_dict[output_k]] = output_param
        params["session"] = sess
        params["graph"] = g

    return params


def test1():
    param_dict = {
        'inputs': {'input_data': 'input_images'},
        'output': {'output': 'seg_maps_pred'}
    }
    model_path = "model/psenet/multi_pb"
    params = restore_model_by_dir(model_path, param_dict['inputs'], param_dict['output'])
    print("asdas")
    return params


def test2():
    print()
    param_dict = {
        'inputs': {'input_image': 'input_image', 'input_im_info': 'input_im_info'},
        'output': {'output_bbox_pred': 'bbox_pred', 'output_cls_prob': 'cls_prob'}
    }

    model_path = "model/ctpn"
    params = restore_model_by_dir(model_path, param_dict['inputs'], param_dict['output'])
    print("asdas")

    t_input_image = params["input_image"]
    t_input_im_info = params["input_im_info"]
    t_bbox_pred = params["bbox_pred"]
    t_cls_prob = params["cls_prob"]
    session = params["session"]
    g = params["graph"]


def test3():
    print()
    param_dict = {
        'inputs': {'input_1': 'input_1', 'input_2': 'input_2', 'input_3': 'input_3'},
        'output': {'output_1': 'output_1', 'output_2': 'output_2', 'output_3': 'output_3', 'output_4': 'output_4',
                   'output_5': 'output_5', 'output_6': 'output_6', 'output_7': 'output_7'}

    }

    model_path = "model/table_detect"
    params = restore_model_by_dir(model_path, param_dict['inputs'], param_dict['output'])
    print("asdas")


if __name__ == '__main__':
    # save_model()
    # p = test1()
    # test2()
    test3()
