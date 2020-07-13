import logging
import time
import os
from utils.rotating_file_handler import SafeRotatingFileHandler

def init(dir,
         level=logging.DEBUG,
         when="D",
         backup=90, # 保持90天
         _format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d行 %(message)s"):

    train_start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = dir+'/ocr.log'
    print("日志文件：", filename)
    _dir = os.path.dirname(filename)
    if not os.path.isdir(_dir):os.makedirs(_dir)

    # 重新设置
    logger = logging.getLogger()

    # 解决console.log上出现垃圾日志的问题：https://github.com/tensorflow/tensorflow/issues/26691
    # import absl.logging
    # logging.root.removeHandler(absl.logging._absl_handler)
    # absl.logging._warn_preinit_stderr = False
    # import absl.logging
    # formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s')
    # absl.logging.get_absl_handler().setFormatter(formatter)
    # stream_logger = logging.getLogger('logger_stream')
    # stream_logger.setLevel(logging.INFO)

    logger.setLevel(level)
    print("设置日志等级：",level)

    formatter = logging.Formatter(_format)

    t_handler = SafeRotatingFileHandler(filename)
    t_handler.setLevel(level)
    t_handler.setFormatter(formatter)
    logger.addHandler(t_handler)
    print("设置日志文件输出方式：",filename,"/",level,"/",when,"/",backup)

    for l in logger.handlers:
        logger.info("当前日志系统的handler：%r",l)