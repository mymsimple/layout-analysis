from service.idcard import idcard_service
from utils import ocr_utils, json_utils
from flask import jsonify, request, Blueprint
import logging, time
from server import conf
from vo.request.ocr_request_vo import OcrRequest, OcrRequestV2
from vo.response.base_response import BaseResponse
from vo.enums.ocr_enum import BizType

logger = logging.getLogger(__name__)

app = Blueprint('ocr_v2', __name__, url_prefix="/v2")
"""
V2.0 OCR相关接口
    1. V2.0 ocr接口：
    2. V2.0 crnn接口：
"""


@app.route('/ocr.ajax', methods=["POST"])
def ocr():
    logger.info("请求url:%r", request.full_path)
    try:
        ocr_request_v2 = OcrRequestV2()
        start = time.time()
        json_utils.json_deserialize(request.get_data(), ocr_request_v2, ignore_null=True)

        # 参数校验
        image = ocr_utils.base64_2_image(ocr_request_v2.img)
        if image is None:
            return jsonify({'error_code': -1, 'message': 'image decode from base64 failed.'})
        height, width, _ = image.shape

        # 注意！ctpn_params是个全局变量，只有在single模式的时候，才会被初始化，否则就是个None
        # TODO !! 检测模型默认！！
        result = idcard_service.process(image)
        logger.debug("识别图片花费[%d]秒", time.time() - start)
        # return jsonify(json_utils.obj2json(response))
        return jsonify(result)
    except Exception as e:

        import traceback
        traceback.print_exc()
        logger.error("处理图片过程中出现问题：%r", e)
        return jsonify(BaseResponse("9999", str(e)).__dict__)


@app.route('/ocr_debug.ajax', methods=["POST"])
def ocr_debug():
    logger.info("请求url:%r", request.full_path)
    try:
        if conf.MODE == "single": conf.disable_debug_flags()  # 不用处理调试的动作，但是对post方式，还是保留
        ocr_request = OcrRequest()
        start = time.time()
        json_utils.json_deserialize(request.get_data(), ocr_request, ignore_null=True)
        logger.info("请求参数：%s", ocr_request)
        # 参数校验
        validate(ocr_request)
        image = ocr_utils.base64_2_image(ocr_request.img)
        if image is None:
            return jsonify({'error_code': -1, 'message': 'image decode from base64 failed.'})
        height, width, _ = image.shape

        # 注意！ctpn_params是个全局变量，只有在single模式的时候，才会被初始化，否则就是个None
        # TODO !! 检测模型默认！！
        success, response = ocr_service.ocr_process(ocr_request,
                                                    conf.MODE)
        logger.debug("识别图片花费[%d]秒", time.time() - start)
        return jsonify(json_utils.obj2json(response))
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error("处理图片过程中出现问题：%r", e)
        return jsonify(BaseResponse("9999", str(e)).__dict__)


def validate(ocr_request: OcrRequest):
    """
       请求参数校验
       :return:
       """
    if not ocr_request.detect_model:
        raise ValueError("detect_model 不能为空")
    if not ocr_request.img:
        raise ValueError("img 不能为空")

