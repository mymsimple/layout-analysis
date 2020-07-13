'''
输入：
	POST JSON格式：
	数据:{
	 'sid':'2019111314040513',
	 'data':'<BASE64编码>',
     'hough_params':{
                'is_user_hough':    true,   # 是否用霍夫变换
                'line_max':         100,    # 霍夫线最大值
                'line_min':         1,      # 霍夫线最小值
                'force':            false,  # 是否强制使用行列
                'force_force':      false,  # 是否强制使用行列切必须行列达到指定数 ???
                'force_row':        false,  # 是否强制行
                'cvt_threshold1':   300,    # 灰度轮廓阀值1
                'cvt_threshold2':   600     # 灰度轮廓阀值2
        }
}

返回：
Json数据
{
   'code':0,
   'msg':'success',
   'rotate':'9.81',
   'image':'<BASE64编码>'
}

错误码说明：
非成功状态，rotate和image可以为空

code汇总：
0 --- 操作成功
9999 --- 系统异常
1001 --- 图像模糊
1002 --- 非纸质流水图片
'''


class HoughParam:
    use_hough: bool  # 是否用霍夫变换
    line_max: int  # 霍夫线最大值
    line_min: int  # 霍夫线最小值
    force: bool  # 是否强制使用行列
    force_force: bool  # 是否强制使用行列切必须行列达到指定数 ???
    force_row: bool  # 是否强制行
    cvt_threshold1: int  # 灰度轮廓阀值1
    cvt_threshold2: int  # 灰度轮廓阀值2


class PreprocessRequest:
    """
      预处理请求报文
    """

    def __init__(self):
        self.sid = ""  # 调用session id
        self.data = ""  # 图片的base64编码
        self.hough_params: HoughParam  #
        self.do_verbose = False  # 是否页面debug

    def __str__(self):
        return "{sid：%s" \
               "data:%r," \
               "hough_params:%r," \
               "do_verbose:%r}" \
               "" % \
               (self.sid,
                len(self.data),
                self.hough_params,
                self.do_verbose
                )


if __name__ == '__main__':
    aa = PreprocessRequest()
    aa.sid = "123"
    aa.data = "asd"
    print(aa)
