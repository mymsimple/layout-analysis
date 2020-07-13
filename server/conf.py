import os, sys, json
import logging
from vo.cfg import system_config as sys_cfg
from utils import json_utils

################################################################
#
#   定义CTPN、CRNN的共同参数
#
################################################################

# 定义相关的目录，这个是为了方便3个项目集成，所以需要绝对路径，方便import，不是为了找文件，找文件用相对路径就好，是为了python import
CTPN_DRAW = True
CTPN_SAVE = False  # 是否保存识别的坐标
CTPN_EVALUATE = False  # 是否提供评估
CTPN_SPLIT = True  # 是否保留小框(CTPN网络识别结果）
CTPN_PRED_DIR = "data/pred"  # 保存的内容存放的目录
CTPN_TEST_DIR = "data/test"  #

# 启动模式：2种
MODE_TFSERVING = "tfserving"
MODE_SINGLE = "single"

# CRNN常用参数
CRNN_BATCH_SIZE = 64
CRNN_INPUT_SIZE = (32, 1024)
CRNN_SEQ_LENGTH = int(CRNN_INPUT_SIZE[1] / 4)
# CRNN_PROCESS_NUM = 2  # 处理CRNN识别的分几个批次

# 通用的调试开关
DEBUG = True

# 全局变量
correcters = None
# 最好做 二级结构 单机版使用的
system_config = sys_cfg.SystemConfig()

logger = logging.getLogger(__name__)
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


# 把没必要的参数都关闭
def disable_debug_flags():
    import tensorflow as tf

    tf.app.flags.FLAGS.remove_flag_values({'evaluate': True})
    tf.app.flags.FLAGS.remove_flag_values({'split': True})
    tf.app.flags.FLAGS.remove_flag_values({'draw': True})
    tf.app.flags.FLAGS.remove_flag_values({'save': True})
    tf.app.flags.DEFINE_boolean('evaluate', False, '')  # 是否进行评价（你可以光预测，也可以一边预测一边评价）
    tf.app.flags.DEFINE_boolean('split', True, '')  # 是否对小框做出评价，和画到图像上
    tf.app.flags.DEFINE_boolean('draw', True, '')  # 是否把gt和预测画到图片上保存下来，保存目录也是pred_home
    tf.app.flags.DEFINE_boolean('save', False, '')  # 是否保存输出结果（大框、小框信息都要保存），保存到pred_home目录里面去


# 初始化和定义各类参数
def init_arguments(conf_file="release_1.0.json"):
    import tensorflow as tf

    if not os.path.exists(conf_file):
        logger.error("系统配置文件不存在：%s", conf_file)
        raise FileExistsError("Config file not exist:" + conf_file)

    json_f = open(conf_file, encoding='utf-8')
    json_data = json.load(json_f)
    json_utils.dic2class_ignore(json_data, system_config)
    print("加载系统配置文件：\n",json.dumps(json_utils.obj2json(system_config),indent=2))

    mode = os.getenv("MODE")
    if mode is None:
        logger.error("未在启动环境变量中设置启动模式MODE")
        raise ValueError("未在启动环境变量中设置启动模式MODE")
        return

    # 赋值给当前模块
    sys.modules[__name__].CFG = system_config
    sys.modules[__name__].MODE = mode  # conf.MODE

    # 接受从环境变量中传入的参数，为什么采用这么诡异的设计，而不是FLAGS呢？
    # 是因为，为了和docker容器启动的方式保持一致，docker方式，变量从环境变量中给出
    # if mode=="tfserving":
    #     logger.info("TFServing模式参数初始化完成")
    #     return

    # 共享的
    tf.app.flags.DEFINE_string('name', 'ocr_web_server', '')  # 是否调试
    tf.app.flags.DEFINE_boolean('debug', DEBUG, '')  # 是否调试

    # 这个是为了兼容 tensorflow flags方式
    # gunicorn -w 2 -k gevent web.api_server:app -b 0.0.0.0:8080
    tf.app.flags.DEFINE_string('worker-class', 'gevent', '')
    tf.app.flags.DEFINE_integer('workers', 1, '')
    tf.app.flags.DEFINE_string('bind', '0.0.0.0:8080', '')
    tf.app.flags.DEFINE_string('env', '', '')
    tf.app.flags.DEFINE_integer('timeout', 60, '')
    tf.app.flags.DEFINE_string('preload', '', '')
    tf.app.flags.DEFINE_integer('worker-connections', 1000, '')

    # ctpn的
    # tf.app.flags.DEFINE_string('ctpn_model', conf.ctpn_model, '')
    tf.app.flags.DEFINE_boolean('evaluate', CTPN_EVALUATE, '')  # 是否进行评价（你可以光预测，也可以一边预测一边评价）
    tf.app.flags.DEFINE_boolean('split', CTPN_SPLIT, '')  # 是否对小框做出评价，和画到图像上
    tf.app.flags.DEFINE_boolean('draw', CTPN_DRAW, '')  # 是否把gt和预测画到图片上保存下来，保存目录也是pred_home
    tf.app.flags.DEFINE_boolean('save', CTPN_SAVE, '')  # 是否保存输出结果（大框、小框信息都要保存），保存到pred_home目录里面去
    tf.app.flags.DEFINE_string('pred_dir', CTPN_PRED_DIR, '')  # 预测后的结果的输出目录
    tf.app.flags.DEFINE_string('test_dir', CTPN_TEST_DIR, '')  # 预测后的结果的输出目录

    # crnn的
    # tf.app.flags.DEFINE_string('crnn_model', conf.crnn_model, '')
    tf.app.flags.DEFINE_string('charset', None, '')
    tf.app.flags.DEFINE_integer('batch_size', CRNN_BATCH_SIZE, '')
    tf.app.flags.DEFINE_string('resize_mode', 'PAD', '')

    logger.info("参数初始化完成,启动模式：%s", mode)


if __name__ == '__main__':
    # Config()
    init_arguments()