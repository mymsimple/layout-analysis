//各页面的输入输出参数项
page_param_json = {
    "ocr.v1": {
        "title": "OCR.V1.0测试结果",
        "url": "ocr",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "do_correct",
                "name_zh": "是否NLP纠错",
                "type": "bool",
            }
        ],
        "output_type": "ocr",
        "output": {}
    },
    "crnn.v1": {
        "title": "crnn.V1.0测试结果",
        "url": "/crnn",
        "input_is_array": true,
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image"
            }
        ],
        "output_type": "crnn"
    },
    "crnn.v2": {
        "title": "crnn.V2.0测试结果",
        "url": "/v2/crnn.ajax",
        "input_is_array": true,
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image"
            }
        ],
        "output_type": "crnn"
    },
    "ocr.v2": {
        "title": "OCR.V2.0测试结果",
        "url": "/v2/ocr.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },{
                "name": "biz_type",
                "name_zh": "业务类型",
                "type": "select",
                "value": {
                    "01": "银行流水",
                    "02": "征信报告",
                }
            },
        ],
        "output_type": "ocr",
        "output": {}
    },
    "ocr.v3": {
        "title": "ocr.V2.0测试结果",
        "url": "v2/ocr_debug.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "do_preprocess",
                "name_zh": "是否预处理",
                "type": "bool",
            },
            {
                "name": "detect_model",
                "name_zh": "检测模型",
                "type": "select",
                "value": {
                    "ctpn": "ctpn",
                    "psenet": "psenet",
                }
            },
            {
                "name": "do_correct",
                "name_zh": "是否NLP纠错",
                "type": "bool",
            },
            {
                "name": "correct_model",
                "name_zh": "纠错模型",
                "type": "select",
                "value": {
                    "bert": "bert",
                    "report_keywords": "征信报告"
                }
            },
            {
                "name": "do_table_detect",
                "name_zh": "是否检测表格",
                "type": "bool",
            },
        ],
        "output": {}
    },
    "plate.v2": {
        "title": "车牌检测结果",
        "url": "/plate.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "imgSign",
                "name_zh": "图片标识",
                "type": "select",
                "value": {
                    "T1": "T1",
                    "T2": "T2"
                }
            },
            {
                "name": "merchantPrimaryKeyId",
                "name_zh": "商户主键id",
                "type": "input"
            },
            {
                "name": "merchantPlate",
                "name_zh": "商户车牌号码",
                "type": "input"
            },
        ],
        "output": {},
        "output_type": "plate"
    },
    "plate.ocr.v2": {
        "title": "车牌小图检测",
        "url": "/plate_ocr.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output": {},
        "output_type": "plate"
    },
    "preprocess.v1": {
        "title": "图片预处理测试结果",
        "url": "/preprocess.ajax",
        "input": [
            {
                "name": "data",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output": {},
        "output_type": "preprocess",

    },
    "detect.v1": {
        "title": "图像检测测试",
        "url": "/detect/detect.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "detect_model",
                "name_zh": "检测模型",
                "type": "select",
                "value": {
                    "ctpn": "ctpn",
                    "psenet": "psenet",
                    "plate": "车牌",
                    "table": "表格",
                    "doc": "图像",
                }
            }, {
                "name": "output_type",
                "name_zh": "输出类型",
                "type": "select",
                "value": {
                    "rect": "外接矩形",
                    "para": "平行四边形",
                    "poly": "多边形",
                }
            },
        ],
        "output": {},
        "output_type": "detect",
    },
    "document.v1": {
        "title": "合同识别",
        "url": "/document.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "do_correct",
                "name_zh": "是否NLP纠错",
                "type": "bool",
            }
        ],
        "output_type": "ocr",
        "output": {}
    },
    "credit.report.split.v1": {
        "title": "征信报告预处理V1",
        "url": "/credit_report/split.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output_type": "credit.report.split",
        "output": {}
    },
    "gjj.v1": {
        "title": "公积金识别V1",
        "url": "/gjj",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output_type": "ocr",
        "output": {}
    },
    "gjj.v2": {
        "title": "公积金识别V2",
        "url": "/gjj.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output_type": "ocr",
        "output": {}
    },
    "correct.v1": {
        "title": "文本纠错V1",
        "url": "/correct",
        "input": [
            {
                "name": "sentences",
                "name_zh": "要纠错的文本",
                "type": "input",
                "is_array": true
            },
            {
                "name": "merchantPrimaryKeyId",
                "name_zh": "商户主键id",
                "type": "input",
            },
        ],
        "output_type": "correct",
        "output": {}
    },
    "binary.v1": {
        "title": "图像二值化",
        "url": "/tools/binary.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "threshold",
                "name_zh": "二值化阈值",
                "type": "input",
            },
        ],
        "output_type": "preprocess",
        "output": {}
    }
}

var g_page_type = "ocr"

function get_element_str(value, image_arr) {
    var temp_str = ""
    if (value.type == 'bool') {
        temp_str += "<input type='hidden' name='" + value.name + "' value=''/>"
        temp_str +=
            "    <a href=\"javascript:;\" class='" + value.name + "' onclick=\"query_bool(true,this,'" + value.name + "');\">是</a>\n" +
            "    <a href=\"javascript:;\" class='" + value.name + "' onclick=\"query_bool(false,this,'" + value.name + "');\">否</a>"

    } else if (value.type == 'select') {
        temp_str += "<input type='hidden' name='" + value.name + "' value=''/>"

        $.each(value.value, function (key, item) {
            temp_str += "<a href=\"javascript:;\" class='" + value.name + "'" +
                " onclick=\"query_select('" + key + "',this,'" + value.name + "');\">" + item + "</a>"
        })
    } else if (value.type == 'image') {
        temp_str += "<input type='hidden' name='" + value.name + "' value=''/>"
        var img_id = value.name + "_file"
        temp_str += '<input type="file" id="' + img_id + '" multiple="multiple" />'
        image_arr.push(value.name)
    } else if (value.type == 'input') {
        temp_str += "<input type='text' name='" + value.name + "' value=''/>"
    }
    return temp_str;
}

/**
 * 输出类型
 * 1. 一张大图多张小图
 * 2. 检测的一张大图，
 */


function init_page(page_type) {
    var input_str = ""
    var page_param = page_param_json[page_type]
    var image_arr = []
    $.each(page_param.input, function (index, value) {
        var temp_str =
            "<dl>" +
            "  <dt>" + value.name_zh + "：</dt>" +
            "  <dd>"
        temp_str += get_element_str(value, image_arr);
        temp_str +=
            "  </dd>" +
            "</dl>"
        input_str += temp_str
    })
    $("#toolbar").prepend(input_str)
    $.each(image_arr, function (i, img_name) {
        init_image(img_name + "_file", img_name)
    })
    if (page_param.title) {
        $("#result_title").html(page_param.title)
    }
    $("#request_url").html("请求url：" + page_param.url)
}

function init_image(image_id, image_name) {
    $("#" + image_id).change(function () {
        var v = $(this).val();
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
        reader.onload = function (e) {
            var result = reader.result.split(",")[1]
            $("input[name='" + image_name + "']").val(result)
        };
    });
}

$(function () {

    // #TODO
    g_page_type = getUrlParam("name")
    init_page(g_page_type)
    $('#submit_ocr').click(function () {
        return submit_ocr();
    });
});

function query_bool(bool_flg, e, cls) {
    $("." + cls).removeClass("btn-primary");
    $(e).addClass("btn-primary");
    $("input[name='" + cls + "']").val(bool_flg)
}

function query_select(select_type, e, cls) {
    $("." + cls).removeClass("btn-primary");
    $(e).addClass("btn-primary");
    $("input[name='" + cls + "']").val(select_type)

}


function submit_ocr() {
    //清空
    $("#small_table  tr:not(:first)").empty("");
    $("#big_image").attr("src", "")

    var param = {}
    param['do_verbose'] = true
    param['sid'] = 'page_sid'
    var page_param = page_param_json[g_page_type]
    $.each(page_param.input, function (index, item) {
        let temp_val = $("input[name='" + item.name + "']").val()
        if (item.type == 'bool') {
            temp_val = JSON.parse(temp_val)
        }
        //数组元素则多拼
        if (item.is_array) {
            param[item.name] = [temp_val]
        } else {
            param[item.name] = temp_val
        }
    })
    //最外侧是数组
    if (page_param.input_is_array) {
        param = [param]
    }

    $.ajax({
        url: page_param.url,
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            if (res.code != '0') {
                alert(res.message)
                $('#result_json').html(syntaxHighlight(res));
                return
            }
            // 成功处理逻辑
            load_result(res)
        },
        error: function (res) {
            // 错误时处理逻辑
            debugger
        }
    });
}


function load_result(result) {
    var output_type = page_param_json[g_page_type].output_type
    // #TODO 输出格式不同，如何做到统一。
    if ("plate" == output_type) {
        load_plate(result)
    } else if ("preprocess" === output_type) {
        load_preprocess(result)
    } else if ('detect' === output_type) {
        load_detect(result)
    } else if ('credit.report.split' === output_type) {
        load_credit_report(result)
    } else if ('correct' === output_type) {
        load_correct(result)
    } else if ('crnn' === output_type) {
        load_crnn(result)
    } else {
        load_ocr(result)
    }
    //展示json
    delete result['debug_info']
    $('#result_json').html(syntaxHighlight(result));
}

function load_crnn(result) {
    $("#text_output").show()
    $("#text_table  tr:not(:first)").empty("");

    var $table = $("#text_table");
    result.prism_wordsInfo.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="90%" align="left">'
            + '<div class="text">' + e.word + '</div>'
            + '</td>'
            + '</tr>'
        $table.append($tr)
    });
}

function load_correct(result) {
    $("#text_output").show()
    $("#text_table  tr:not(:first)").empty("");

    var $table = $("#text_table");
    result.sentences.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="90%" align="left">'
            + '<div class="text">' + e + '</div>'
            + '</td>'
            + '</tr>'
        $table.append($tr)
    });
}

function load_credit_report(result) {
    $("#report_output").show()
    $("#report_image").attr("src", "data:image/jpg;base64," + result.image)
    var small_images = result['split_images']

    var $table = $("#report_table");
    small_images.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="90%" align="left"><img style="min-height:20px;max-width:95%" src="data:image/jpg;base64,' + e + '"></td>'
            + '</tr>'
        $table.append($tr)
    });

}

function load_detect(result) {
    $("#detect_output").show()
    //清空
    $("#detect_table  tr:not(:first)").empty("");
    $("#detect_image").attr("src", "")
    $("#detect_output").show()
    $("#detect_image").attr("src", "data:image/jpg;base64," + result.image)
    var small_images = result['small_images']
    var $table = $("#detect_table");
    small_images.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="70%" align="left"><img style="min-height:20px;max-width:95%" src="data:image/jpg;base64,' + e + '"></td>'
            + '<td width="30%" style="WORD-WARP:break-word">' + result['boxes'][i] + '</td>'
            + '</tr>'
        $table.append($tr)
    });
}

function load_preprocess(result) {
    $("#preprocess_output").show()
    $("#pre_image").attr("src", "data:image/jpg;base64," + result.image)
}

function load_ocr(result) {
    $("#ocr_output").show()
    var debug_info = result.debug_info
    $("#big_image").attr("src", "data:image/jpg;base64," + debug_info.image)
    var $table = $("#small_table");
    var small_images = debug_info['small_images']
    small_images.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="60%" align="left"><img style="min-height:20px;max-width:95%" src="data:image/jpg;base64,' + e + '"></td>'
            + '<td width="20%">' + debug_info['text'][i] + '</td>'
            + '<td>' + debug_info['text_corrected'][i] + '</td>'
            + '</tr>'
        $table.append($tr)
    });
}

function load_plate(result) {
    $("#plate_output").show()
    if (result.debug_info != null) {
        var debug_info = result.debug_info
        $("#plate_no").html(result.plate.plate)
        $("#plate_image").attr("src", "data:image/jpg;base64," + debug_info.image)
        $("#plate_small").attr("src", "data:image/jpg;base64," + debug_info.plate_image)
    }

}


function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
        function (match) {
            var cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        }
    );
}

//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
}

a = ["123", "456"]
a = [{"img": "123"}, {"img": "456"}]