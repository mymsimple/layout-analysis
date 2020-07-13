from flask import jsonify, request, abort, render_template, Response
import logging, json, base64

logger = logging.getLogger(__name__)

'''
    Web服务的基类
'''
class WebProcessor():
    def __init__(self, name):
        self.name = name

    # 网页命名规则
    def get_web_index_url(self):
        return "/" + self.name

    # 得到restful的地址，用于flask url注册
    def get_resful_url(self):
        return "/" + self.name

    # 得到web post的地址，用于flask url注册
    def get_web_post_url(self):
        return "/" + self.name + '.post'

    # web展示结果的页面模板名称
    def get_post_result_page_name(self):
        return self.name + "_result.html"

    # 某个业务的首页模板名称
    def web_index(self):
        return render_template(self.name + "_index.html")

    # 网页上post后的处理
    def web_post(self):
        pass

    # Restful 调用后的处理
    def restful(self):
        pass
