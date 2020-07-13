from vo.request.base_request_vo import ImageBaseRequest


class DetectRequest(ImageBaseRequest):
    """
        图像检测 请求报文
    """
    # 检测model（ctpn/psenet等）
    detect_model = ''
    # 输出类型 rect para poly
    output_type = "rect"
    # 二值化阈值
    threshold = None
    # 图片识别前是否做矫正处理
    do_preprocess = False

    def __str__(self):
        return "sid：%s" \
               "detect_model:%s," \
               "output_type:%r," \
               "threshold:%s," \
               "do_verbose:%r," \
               "do_preprocess:%r," \
               "img:%r," \
               "" % \
               (self.sid,
                self.detect_model,
                self.output_type,
                self.threshold,
                self.do_verbose,
                self.do_preprocess,
                len(self.img))
