class PlateRequest:
    """
    车牌识别请求报文
    """
    sid = ""  # 调用session id
    img = ""  # 图片的base64编码
    imgSign = ""  # 图片标识 T1 T2
    merchantPrimaryKeyId = ""  # 商户主键id
    merchantPlate = ""  # 商户车牌号码'
    do_verbose = False

    def __str__(self):
        return "sid：%s" \
               "img:%r," \
               "imgSign:%r," \
               "merchantPrimaryKeyId:%r," \
               "merchantPlate:%r," \
               "do_verbose:%r," \
               "" % \
               (self.sid,
                len(self.img),
                self.imgSign,
                self.merchantPrimaryKeyId,
                self.merchantPlate,
                self.do_verbose
                )
