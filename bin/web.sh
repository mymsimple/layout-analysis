#!/usr/bin/env bash

function help(){
    echo "命令格式："
    echo "  server.sh start --port|-p [默认8080] --worker|-w [默认3] --gpu [0|1] --mode|-m [tfserving|single]"
    echo "  server.sh stop"
    echo "  例：bin/server.sh start -p 8080 -w 1 -g 3 -m single"
    exit
}

if [ "$1" = "stop" ]; then
    echo "停止 OCR Web 服务"
    ps aux|grep ocr_web_server|grep -v grep|awk '{print $2}'|xargs kill -9
    exit
fi

if [ -z "$*" ]; then
    help
    exit
fi

if [ "$1" = "debug" ]; then
    echo "OCR Web 服务调试模式"
    MODE=single gunicorn --workers=1 --name=ocr_web_server --bind=0.0.0.0:8080 --timeout=300 server.server:app
    exit
fi

if [ ! "$1" = "start" ]; then
    help
    exit
fi

echo "启动 OCR Web 服务器..."
Date=$(date +%Y%m%d%H%M)
ARGS=`getopt -o p:m: --long port:,mode: -n 'help.bash' -- "$@"`
eval set -- "${ARGS}"
while true ;
do
        case "$1" in
                -p|--port)
                    echo "自定义端口号：$2"
                    if ! [ $PORT ]; then PORT=$2; fi #如果已经在环境变量中定义了，则不覆盖，环境变量优先级最大！！！这个是为了兼容容器方式启动，因为容器方式只能通过环境变量传入这些参数
                    shift 2
                    ;;
                -m|--mode)
                    echo "自定义模式：  $2"
                    if ! [ $MODE ]; then MODE=$2; fi
                    shift 2
                    ;;

                --) shift ; break ;;
                *) help; exit 1 ;;
        esac
done

if [ $? != 0 ]; then
    help
    exit 1
fi

if [ $? != 0 ]; then
    help
    exit 1
fi

 PORT=8080
 MODE=single

echo "环境变量："
echo "-------------------"
echo "PROT:$PORT"
echo "MODE:$MODE"
echo "-------------------"

# 如果外部环境变量和参数中都没有定义port或者mode，给予默认值
if ! [ $PORT ]; then
    echo "未定义PORT，给予默认值：8080"
    PORT=8080
fi
if ! [ $MODE ]; then
    echo "未定义MODE，给予默认值：tfserving"
    MODE=tfserving
fi

# 针对模式设置worker数，single模式不能太多，只能为3，防止显存OOM
if [ "$MODE" == "tfserving" ]; then
    echo "服务器TfServing模式启动..."
    # gunicorn不支持扩展参数，所以只能靠环境变量传参进去 --env
    # >/dev/null 2>&1 &
    _CMD="MODE=$MODE gunicorn \
        --workers=10 \
        --timeout=300 \
        --bind 0.0.0.0:$PORT \
        --name=ocr_web_server \
        server.server:app >../logs/console.log 2>&1"
    echo "启动服务："
    echo "$_CMD"
    eval $_CMD
    exit 0
fi

if [ "$MODE" == "single" ]; then
    echo "服务器Single模式启动..."
    # 参考：https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
    # worker=3是根据GPU的显存数调整出来的，ration=0.2，大概一个进程占满为2.5G,4x2.5=10G显存
    _CMD="MODE=$MODE gunicorn \
        --name=ocr_web_server \
        --workers=1 \
        --bind 0.0.0.0:$PORT \
        --timeout=300 \
        server.server:app
#        >../logs/console.log 2>&1"
    echo "启动服务："
    echo "$_CMD"
    eval $_CMD
    exit 0
fi

echo "无法识别的服务器类型：MODE=[$MODE]"