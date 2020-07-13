from vo.request.base_request_vo import ImageBaseRequest


class BinaryRequest(ImageBaseRequest):
    """
    二值化请求报文
    """
    # 二值化阈值
    threshold = None

    def __str__(self):
        return "sid：%s" \
               "threshold:%r," \
               "img:%r," \
               "" % \
               (self.sid,
                self.threshold,
                len(self.img))
