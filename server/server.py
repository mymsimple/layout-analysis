import os, logging, traceback
from flask import Flask, render_template
from werkzeug.routing import BaseConverter
from threading import current_thread

from service.server import server_utils
from utils import logger as log
from server import conf


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


# 参考：https://www.cnblogs.com/haolujun/p/9778939.html
# gc.freeze() #调用gc.freeze()必须在fork子进程之前，在gunicorn的这个地方调用正好合适，freeze把截止到当前的所有对象放入持久化区域，不进行回收，从而model占用的内存不会被copy-on-write。
# app = Flask(__name__,static_folder="./web/static",template_folder="./web/templates")
app = Flask(__name__, root_path=os.path.join(os.getcwd(), "web"))
app.jinja_env.globals.update(zip=zip)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.url_map.converters['regex'] = RegexConverter


def _logger():
    return logging.getLogger("WebServer")


@app.errorhandler(500)
def internal_server_error_500(e):
    print("异常发生：")
    traceback.print_exc()
    _logger().error("====================================异常堆栈为====================================", exc_info=True)
    _logger().info("==================================================================================")


@app.route("/")
def index():
    version = server_utils.get_version()
    return render_template('index.html', version=version)


@app.route('/<regex(".*.html"):url>')
def html_request(url):
    """
    url: html url
    """
    _logger().info("请求页面：%r", url)
    return render_template(url)

def init_log():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

def startup(app):
    conf.init_arguments()
    # log.init(conf.system_config.log_dir)
    init_log()
    _logger().debug('启动模式：%s,子进程:%s,父进程:%s,线程:%r', conf.MODE, os.getpid(), os.getppid(), current_thread())

    # 初始化各种变量（全局）
    server_utils.init_single(conf.MODE)

    # 注册所有蓝图
    regist_blueprint(app)
    _logger().info("注册完所有路由：\n %r", app.url_map)
    _logger().info("系统启动完成")


def regist_blueprint(app):
    """
     注册所有蓝图 TODO  想办法如何一键式解决,保证开闭
    :param app:
    :return:
    """
    from server.controller import idcard_controller
    app.register_blueprint(idcard_controller.app)


print("启动服务器...")
startup(app)
