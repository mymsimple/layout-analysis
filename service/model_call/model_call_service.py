#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from utils import tf_serving_agent
import logging
from vo.cfg.system_config import ModelParamConfig

logger = logging.getLogger(__name__)


class BaseCall(metaclass=ABCMeta):

    def __init__(self, call_mode, model_param=None):
        """
        :param call_mode: 调用模式（tfserving/直接调用）
        :param model_param: 模型配置参数
        """
        model_param: ModelParamConfig
        self.model_param = model_param
        self.__call_mode = call_mode

    def call(self, data, params=None):
        """
        调用model
        :param data: 模型输入参数(多个参数做成list或者tuple)，一定要注意多个参数顺序要和
        :param params: single预测时的参数
        :return:
        """
        # TODO data参数校验
        if self.__call_mode == 'tfserving':
            logger.debug("%r-调用TFServing进行预测-%r", self.__class__.__name__,self.model_param.name)
            return self.call_tfserving(data, params)
        else:
            logger.debug("%r-调用本地模型进行预测-%r", self.__class__.__name__,self.model_param.name)
            return self.call_single(data, params)

    # @abstractmethod
    def call_tfserving(self, data, params):
        return tf_serving_agent.tf_serving_call(data, self.model_param)

    # @abstractmethod
    def call_single(self, data, params):
        # 还原各类张量
        params = self.model_param.model_params
        session = params["session"]
        g = params["graph"]
        inputs = {}
        for i, value in enumerate(self.model_param.input):
            logger.debug("输入参数：%r", value.name)
            inputs[params[value.name]] = data[i]
        outputs = []
        for value in self.model_param.output:
            outputs.append(params[value.name])

        with g.as_default():
            output_pred = session.run(outputs, feed_dict=inputs)
            return output_pred


class CorrectCall(BaseCall):
    """
     纠错 模型调用
    """
    pass


class PsenetCall(BaseCall):
    """
     psenet 模型调用
    """

    def __init__(self, call_mode, model_param, output_type):
        # 覆盖父类构造函数
        super().__init__(call_mode, model_param)
        # 标识输出类型
        self.output_type = output_type

    # def call_tfserving(self, images, params):
    #     return tf_serving_agent.psenet_tf_serving_call(self.model_param.name, images[0])

    # def call_single(self, images, params):
    #     # 还原各类张量
    #     t_input_images = params["input_images"]
    #     t_seg_maps_pred = params["seg_maps_pred"]
    #     session = params["session"]
    #     g = params["graph"]
    #     with g.as_default():
    #         # logger.debug("通过session预测：%r",img.shape)
    #         seg_maps = session.run(t_seg_maps_pred, feed_dict={t_input_images: images})
    #     # 预测出来和原图是4倍关系
    #     return seg_maps


class PlateOcrCall(BaseCall):
    """
     车牌识别 模型调用
    """
    pass
    # def call_tfserving(self, images, params):
    #     # 多图一起预测
    #     return tf_serving_agent.plate_ocr_tf_serving_call(images)
    #
    # def call_single(self, images, params):
    #     # 还原各类张量
    #     t_input_x = params["input_x"]
    #     t_output_x = params["output_x"]
    #     session = params["session"]
    #     g = params["graph"]
    #     with g.as_default():
    #         # logger.debug("通过session预测：%r",img.shape)
    #         output_cls = session.run(t_output_x, feed_dict={t_input_x: images})
    #     # TODO 名字暂这样命名
    #     return output_cls


class RotateCall(BaseCall):
    """
     图片旋转 模型调用
    """
    pass


class CrnnCall(BaseCall):
    """
     Crnn 模型调用
    """
    pass


class CtpnCall(BaseCall):
    """
     Ctpn 模型调用 TODO 尚未实现
    """
    pass


class MaskRcnnCall(BaseCall):
    """
     MaskRcnn 模型调用
    """
    pass


if __name__ == '__main__':
    # //
    print()
    # print("a")
    # a.call("dasd","asd")
