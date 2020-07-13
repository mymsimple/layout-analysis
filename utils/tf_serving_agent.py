# # -*- coding: utf-8 -*-
# """
#     说明：
# """
# from server import conf
# from server.conf import system_config
# import logging
# import numpy as np
#
# import tensorflow as tf
# import grpc
# from tensorflow.contrib.util import make_tensor_proto
# from tensorflow_serving.apis import predict_pb2
# from tensorflow_serving.apis import prediction_service_pb2_grpc
# from vo.cfg.system_config import ModelParamConfig
#
# logger = logging.getLogger(__name__)
#
#
# # TODO !! 这里也配置封装
# def create_channel(name, IP, PORT):
#     logger.info("TF Serving 通道连接 - name:%s IP:%s PORT:%s", name, IP, PORT)
#     # 报文大小限制
#     options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
#                ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
#     channel = grpc.insecure_channel("{}:{}".format(IP, PORT), options=options)
#     stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
#
#     # 预测请求
#     request = predict_pb2.PredictRequest()
#     request.model_spec.name = name
#     request.model_spec.signature_name = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
#     logger.info("链接模型[%s]的通道创建,IP:%s,端口:%s,", name, IP, PORT)
#
#     return stub, request
#
#
# def tf_serving_call(data, model_param: ModelParamConfig):
#     stub, request = create_channel(model_param.name, system_config.tfserving_ip, system_config.tfserving_port)
#
#     for i, v in enumerate(model_param.input):
#         logger.info("%r模型输入参数赋值：%r", model_param.name, v.name)
#         # if i == 0: TODO
#         if "" == v.type:
#             request.inputs[v.name].CopyFrom(make_tensor_proto(np.array(data[i])))
#         elif "float32" == v.type:
#             request.inputs[v.name].CopyFrom(make_tensor_proto(np.array(data[i]), dtype=tf.float32))
#         elif "int32" == v.type:
#             request.inputs[v.name].CopyFrom(make_tensor_proto(np.array(data[i]), dtype=tf.int32))
#         else:
#             request.inputs[v.name].CopyFrom(make_tensor_proto(data[i]))
#
#     logger.debug("调用%s 模型预测，开始：调用TF-Server，IP：%s,端口：%s", model_param.name, system_config.tfserving_ip,
#                  system_config.tfserving_port)
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用%r模型预测，结束", model_param.name)
#
#     results = {}
#     for key in response.outputs:
#         logger.debug("%r模型返回参数：%r", model_param.name, key)
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#     outputs_pred = []
#     for v in model_param.output:
#         # 从模型中出来的参数是key
#         outputs_pred.append(results[v.name])
#     return outputs_pred
#
#
# def crnn_tf_serving_call(_input_data, _batch_size_array, model_name="crnn"):
#     stub, request = create_channel(model_name, system_config.tfserving_ip, system_config.tfserving_port)
#
#     request.inputs["input_data"].CopyFrom(make_tensor_proto(np.array(_input_data), dtype=tf.float32))
#     request.inputs["input_batch_size"].CopyFrom(make_tensor_proto(_batch_size_array))
#
#     logger.debug("调用CRNN模型预测，开始：调用TF-Server，IP：%s,端口：%d", system_config.tfserving_ip, system_config.tfserving_port)
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用CRNN模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         logger.debug("CRNN模型返回参数：%r", key)
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     # output_net_out_index = results["output_net_out_index"]
#     # B(output_net_out_index)
#     # logger.info("output_net_out_index:%s", output_net_out_index)
#     # logger.info("output_net_out_index.shape:%s", output_net_out_index.shape)
#     # logger.debug("output_indices.shape:%s", output_indices.shape)
#     # logger.debug("output_shape.shape:%s", output_shape.shape)
#     # logger.debug("output_values.shape:%s", output_values.shape)
#     # preds_sparse = tf.SparseTensor(output_indices, output_values, output_shape)
#
#     # A.解决单个SparseTensor无法被识别的问题，红岩之前的解决方案
#     output_indices = results["output_indices"]
#     output_values = results["output_values"]
#     output_shape = results["output_shape"]
#
#     # v1版只返回3个参数
#     if model_name == 'crnn':
#         return output_indices, output_values, output_shape
#
#     output_pred = results["output_pred"]
#     output_prob = results["output_prob"]
#
#     return output_indices, output_values, output_shape, output_pred, output_prob
#
#
# def ctc_call(_input_data, charset):
#     _batch_size_array = np.array(len(_input_data) * [conf.CRNN_SEQ_LENGTH]).astype(np.int32)
#     output_indices, output_values, output_shape = crnn_tf_serving_call(_input_data, _batch_size_array)
#     pred = __sparse_tensor_to_str(output_indices, output_values, output_shape, charset)
#     return pred
#
#
# # 把返回的稀硫tensor，转化成对应的字符List
# def __sparse_tensor_to_str(indices, values, dense_shape, characters):
#     values = np.array([characters[id] for id in values])
#
#     number_lists = np.array([['\n'] * dense_shape[1]] * dense_shape[0], dtype=values.dtype)
#     res = []
#
#     for i, index in enumerate(indices):
#         number_lists[index[0], index[1]] = values[i]
#
#     for one_row in number_lists:
#         res.append(''.join(c for c in one_row if c != '\n'))
#
#     return res
#
#
# # 并发来实现crnn调用
# #
# # 原因是：crnn中的ctc占用时长太长，
# #
# # 我们想并发，尝试了多进程，失败，总是报一个""错，
# # 尝试多线程，运行ok，但是并没有提升速度，还是36秒，怀疑是服务端还是串行
# # 后来发现了tfserving client就支持异步调用方式，尝试后，调用速度可以了，但是等每个异步都结束，还是慢，36秒。
# #
# # 此方法暂做保留，留作参考 2019.12 piginzoo
# def crnn_tf_serving_call_concurrency(split_images, charset):
#     futures = []
#     for i, images in enumerate(split_images):
#         _batch_size_array = np.array(len(images) * [conf.CRNN_SEQ_LENGTH]).astype(np.int32)
#
#         stub, request = create_channel(system_config.crnn_params.name, system_config.tfserving_ip,
#                                        system_config.tfserving_port)
#
#         request.inputs["input_data"].CopyFrom(make_tensor_proto(np.array(images), dtype=tf.float32))
#         request.inputs["input_batch_size"].CopyFrom(make_tensor_proto(_batch_size_array))
#
#         logger.debug("[%d]调用CRNN模型预测，开始：调用TF-Server，IP：%s,端口：%d", i, system_config.tfserving_ip,
#                      system_config.tfserving_port)
#
#         response_future = stub.Predict.future(request, 60.0)
#
#         futures.append(response_future)
#
#     logger.debug("调用CRNN模型预测，结束")
#
#     preds = []
#     for future in futures:
#         response = future.result()
#         results = {}
#         for key in response.outputs:
#             logger.debug("CRNN模型返回参数：%r", key)
#             tensor_proto = response.outputs[key]
#             results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#         output_indices = results["output_indices"]
#         output_values = results["output_values"]
#         output_shape = results["output_shape"]
#         pred = __sparse_tensor_to_str(output_indices, output_values, output_shape, charset)
#         preds.append(pred)
#
#     return preds
#
#
# def ctpn_tf_serving_call(image, im_info):
#     stub, request = create_channel(system_config.ctpn_params.name, system_config.tfserving_ip,
#                                    system_config.tfserving_port)
#
#     request.inputs["input_image"].CopyFrom(make_tensor_proto(np.array([image]), dtype=tf.float32))
#     request.inputs["input_im_info"].CopyFrom(make_tensor_proto(np.array([im_info]), dtype=tf.float32))
#     logger.debug("调用CTPN模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用CTPN模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     cls_prob = results["output_cls_prob"]
#     bbox_pred = results["output_bbox_pred"]
#     return bbox_pred, cls_prob
#
#
# def preprocess_tf_serving_call(images):
#     stub, request = create_channel(system_config.preprocess_params.name, system_config.tfserving_ip,
#                                    system_config.tfserving_port)
#
#     request.inputs["x"].CopyFrom(make_tensor_proto(np.array(images), dtype=tf.float32))
#     logger.debug("调用预处理模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用预处理模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     cls_prob = results["predCls"]
#     logger.debug("预处理模型返回：%r", cls_prob)
#     return cls_prob
#
#
# def plate_detect_tf_serving_call(image):
#     stub, request = create_channel(system_config.plate_detect_params.name, system_config.tfserving_ip,
#                                    system_config.tfserving_port)
#
#     request.inputs["input_data"].CopyFrom(make_tensor_proto(np.array([image]), dtype=tf.float32))
#     logger.debug("调用车牌检测模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用车牌检测模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     # logger.debug("车牌检测返回：%r",results)
#     cls_prob = results["output"]
#     return cls_prob
#
#
# def plate_ocr_tf_serving_call(image):
#     stub, request = create_channel(system_config.plate_ocr_params.name, system_config.tfserving_ip,
#                                    system_config.tfserving_port)
#
#     request.inputs["input"].CopyFrom(make_tensor_proto(np.array(image), dtype=tf.float32))
#     logger.debug("调用车牌号码识别模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用车牌号码识别模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     # logger.debug("车牌号码识别模型返回：%r",results)
#     cls_prob = results["output"]
#     return cls_prob
#
#
# def psenet_tf_serving_call(model_name, image):
#     """
#      psenet tfserving调用
#     :param model_name: psenet训练的不同模型的名称
#     :param image:
#     :return:
#     """
#     stub, request = create_channel(model_name, system_config.tfserving_ip, system_config.tfserving_port)
#     request.inputs["input_data"].CopyFrom(make_tensor_proto(np.array([image]), dtype=tf.float32))
#     logger.debug("调用psenet检测模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用psenet检测模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     # logger.debug("车牌检测返回：%r",results)
#     cls_prob = results["output"]
#     return cls_prob
#
#
# def mask_rcnn_tf_serving_call(model_name, molded_images_list,
#                               image_metas_list,
#                               anchors):
#     """
#      mask rcnn tfserving调用
#     :param anchors:
#     :param molded_images_list:
#     :param image_metas_list:
#     :param model_name: mask训练的不同模型的名称 table
#     :param image:
#     :return:
#     """
#     stub, request = create_channel(model_name, system_config.tfserving_ip, system_config.tfserving_port)
#     request.inputs["input_1"].CopyFrom(make_tensor_proto(np.array(molded_images_list), dtype=tf.float32))
#     request.inputs["input_2"].CopyFrom(make_tensor_proto(np.array(image_metas_list), dtype=tf.float32))
#     request.inputs["input_3"].CopyFrom(make_tensor_proto(np.array(anchors), dtype=tf.float32))
#     logger.debug("调用mask rcnn 检测模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用mask rcnn t检测模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         tensor_proto = response.outputs[key]
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#
#     return results["output_1"], results["output_2"], results["output_3"], results["output_4"], \
#            results["output_5"], results["output_6"], results["output_7"]
#
#
# def correct_tf_serving_call(batch, sess=None):
#     stub, request = create_channel(system_config.correct_config.name, system_config.tfserving_ip,
#                                    system_config.tfserving_port)
#
#     input_ids, input_mask, segment_ids, masked_lm_positions, masked_lm_ids, masked_lm_weights, _ = batch
#
#     request.inputs["input_ids"].CopyFrom(make_tensor_proto(np.array(input_ids), dtype=tf.int32))
#     request.inputs["input_mask"].CopyFrom(make_tensor_proto(np.array(input_mask), dtype=tf.int32))
#     request.inputs["segment_ids"].CopyFrom(make_tensor_proto(np.array(segment_ids), dtype=tf.int32))
#     request.inputs["masked_lm_positions"].CopyFrom(make_tensor_proto(np.array(masked_lm_positions), dtype=tf.int32))
#     request.inputs["masked_lm_ids"].CopyFrom(make_tensor_proto(np.array(masked_lm_ids), dtype=tf.int32))
#     request.inputs["masked_lm_weights"].CopyFrom(make_tensor_proto(np.array(masked_lm_weights), dtype=tf.float32))
#
#     logger.debug("调用纠错识别模型预测，开始")
#     response = stub.Predict(request, 60.0)
#     logger.debug("调用纠错识别模型预测，结束")
#
#     results = {}
#     for key in response.outputs:
#         # logger.debug("开始获取tensor")
#         tensor_proto = response.outputs[key]
#         # logger.debug("开始解析tensor,tf.contrib.util.make_ndarray:%s", key)
#         results[key] = tf.contrib.util.make_ndarray(tensor_proto)
#         logger.debug("解析tensor完成")
#     topn_probs = results["topn_probs"]
#     topn_predictions = results["topn_predictions"]
#
#     return np.array(topn_probs, dtype=float), topn_predictions
