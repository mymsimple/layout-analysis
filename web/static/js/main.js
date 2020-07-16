//各页面的输入输出参数项
page_param_json = {
    "idcard.ocr.v1": {
        "title": "身份证识别",
        "url": "/idcard/ocr.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            }
        ],
        "output_type": "idcard",
        "output": {}
    }
}
//"output_type": "text_only"

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
    debugger
    if ("idcard" == output_type) {

        load_idcard(result)
    }
    //展示json
    delete result['debug_info']
    $('#result_json').html(syntaxHighlight(result));
}


function load_idcard(result) {
    $("#idcard_output").show()
//    $("#report_image").attr("src", "data:image/jpg;base64," + result.image)
    var data = result['data']

    var $table = $("#idcard_table");
    data.forEach(function (e, i, array) {
        var $tr = '<tr>'
            + '<td width="30%" style="WORD-WARP:break-word">' + e.name + '</td>'
            + '<td width="30%" style="WORD-WARP:break-word">' + e.value + '</td>'
            + '</tr>'
        $table.append($tr)
    });

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