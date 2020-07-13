from vo.request.base_request_vo import ImageBaseRequest


class OcrRequest:
    """
    OCR 请求报文
    """
    # 请求id
    sid = ""
    # 要识别的图片（base64格式）
    img = ''
    # 检测model（ctpn/psenet等） 默认ctpn
    detect_model = 'ctpn'
    # 识别模型 crnn/crnn.v2
    recognize_model = 'crnn.v2'
    # 业务类型 'report','bankflow'
    business_type = 'report'
    # 二值化阈值
    threshold = None
    # 是否返回debug图片
    do_verbose = False
    # 图片识别前是否做矫正处理
    do_preprocess = False
    # 识别之后是否做文字矫正
    do_correct = False
    # 是否做版面行分析
    do_layout = False
    # 是否做表格检测
    do_table_detect = False

    def __str__(self):
        return "sid：%s" \
               "detect_model:%s," \
               "threshold:%r," \
               "do_verbose:%r," \
               "do_correct:%r," \
               "do_layout:%r," \
               "img:%r," \
               "" % \
               (self.sid,
                self.detect_model,
                self.threshold,
                self.do_verbose,
                self.do_correct,
                self.do_layout,
                len(self.img))


class OcrRequestV1:
    """
    OCR 请求报文V1.0 版本
    """
    # 之前没有此要求
    sid = ""
    # 要识别图片的url
    url = ""
    # 要识别的图片（base64格式）
    img = ''
    do_verbose = False
    do_correct = False


class OcrRequestV2(ImageBaseRequest):
    """
    OCR 请求报文V2.0 版本
    """
    # 业务类型 ：默认 征信报告？
    biz_type = "02"


if __name__ == '__main__':
    req = OcrRequest()
    req.do_layout = False
    # req.detect_model="psenet"

    # print(req.__str__())
    # print(req)
    # logger.info("qingca shu:%s",req)
