"""
系统参数配置
"""


class PreprocessConfig:
    """
        预处理配置
    """
    name = "default"
    # 预测出来的顺序对应的角度
    class_name = [0, 90, 180, 270]
    do_vgg = False
    # 小图片最多个数
    max_counter = 32
    # 是否标准化
    do_std = True
    # 多少一下的过滤掉
    nms_box_cnt = 5
    nms_min_area = 20
    nms_max_area = 600
    # 对IOU>0.3的进行NMS筛选，剩下的是靠谱的框（在remains里面）
    nms_iou = 0.3

    # 是否去除边缘
    do_crop_edge = False
    crop_edge_percent = 0.05

    #
    preprocess_blur = False
    preprocess_valid = True
    preprocess_tuning = True


class ModelParamMapping:
    """
    模型输入输出参数配置
    """

    def __init__(self):
        # 模型中的变量名
        self.name = ""
        # 转换后起的别名、本机启动模式用这个名取值
        self.alias = ""
        # 字段数据类型，在tfserving调用时要做转换
        # 00: 不做处理
        # 01：dtype=tf.int32
        # 02:dtype=tf.float32
        self.type = ""

class ModelParamConfig(object):
    """
    配置模型加载的输入输出参数
    """

    # # 模型名
    # name = ""
    # # 模型路径
    # model_path = ""
    # # input 的key是模型里的变量，value是本地模式启之后的参数参数变量。
    # input = []
    # output = []
    # # 模型参数，single模式启动时把模型加载到此变量中
    # model_params = None

    def __init__(self):
        # 模型名
        self.name = ""
        # 模型路径
        self.model_path = "model/table_detect/100000/"
        # input 的key是模型里的变量，value是本地模式启之后的参数参数变量。
        self.input = [ModelParamMapping]
        self.output = [ModelParamMapping]
        # 模型参数，single模式启动时把模型加载到此变量中
        self.model_params = None


class CrnnParamConfig(ModelParamConfig):
    # 字符集名称
    charset_name = ""


class KwdsCorrecterConfig:
    """
    关键字纠错的配置
    """
    prob_threshold = 0.9
    similarity_threshold = 0.6
    char_meta_file = ''
    key_words_file = ''


class BertCorrecterConfig:
    prob_threshold = 0.9
    max_seq_length = 64
    topn = 3
    batch_size = 16
    char_meta_file = ""
    vocab_file = "vocab.txt"
    bert_config_file = "bert_config.json"


class CorrecterConfig(ModelParamConfig):
    """
    纠错相关的配置
    """
    report_config = KwdsCorrecterConfig()
    gongjijin_config = KwdsCorrecterConfig()
    bert_config = BertCorrecterConfig()


class SystemConfig:
    """
    总配置
    """
    tfserving_port = "8500"
    tfserving_ip = "15.15.52.10"
    log_dir = "../logs"
    data_dir = "/home/ocr/data"

    # 预处理相关配置
    preprocess_config = PreprocessConfig()
    charsets = {}
    # 各模型输入输出参数
    # 纠错相关配置
    correct_config = CorrecterConfig()
    ctpn_params = ModelParamConfig()
    crnn_params = CrnnParamConfig()
    crnn_v2_params = CrnnParamConfig()
    plate_ocr_params = ModelParamConfig()
    plate_detect_params = ModelParamConfig()
    psenet_params = ModelParamConfig()
    preprocess_params = ModelParamConfig()
    table_detect_params = ModelParamConfig()


if __name__ == '__main__':
    print("")
    from utils import json_utils
    import json

    f = open("release_1.0.json", encoding='utf-8')
    json_data = json.load(f)
    print("配置：", json_data)
    config = SystemConfig()
    # json_data = setting
    json_utils.dic2class_ignore(json_data, config)
    print(config.preprocess_params.input[0])
    xxx = config.preprocess_params.input[0]
    print(xxx.get_alias())
    json_file = json_utils.obj2json(config)
    # print(json_file)
    # print(json.dumps(config, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=False,
    #                     indent=4))
