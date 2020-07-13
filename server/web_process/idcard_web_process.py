from server.web_processor.web_processor import WebProcessor
from utils import ocr_utils, api
from service.idcard import idcard_service as service
from flask import jsonify, request, abort, render_template, Response
import logging, time
from server import conf

logger = logging.getLogger(__name__)


class IDCardWebProcessor(WebProcessor):

    def web_post(self):
        data = request.files['image']
        image_name = data.filename
        buffer = data.read()
        image = ocr_utils.bytes2image(buffer)
        if image is None:
            abort(500)
            abort(Response('解析Web传入的图片失败'))

        logger.debug("获得上传图片[%s]，尺寸：%d 字节", image_name, len(image))
        start = time.time()
        result, small_images, bboxes = service.process(image)

        # 准备Web测试用的显示数据
        result['small_images'] = ocr_utils.nparray2base64(small_images)
        ocr_utils.draw_bboxes(image,bboxes)
        result['image'] = ocr_utils.nparray2base64(image)

        logger.debug("识别图片[%s]花费[%d]秒", image_name, time.time() - start)

        return render_template(self.get_post_result_page_name(), result=result)

    def restful(self):

        try:
            buffer, sid = api.process_request(request)
            image = ocr_utils.bytes2image(buffer)
            if image is None:
                return jsonify({'error_code': -1, 'message': 'image decode from base64 failed.'})

            height, width, _ = image.shape

            result, small_images, bboxes = service.process(image)

            results = api.post_process(sid, result, None, None, width, height)

            return jsonify(results)

        except Exception as e:
            logger.exception("处理图片过程中出现问题：%r", e)
            return jsonify({'error_code': -1, 'message': str(e)})
