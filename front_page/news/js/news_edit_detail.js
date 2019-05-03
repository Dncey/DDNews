var token = sessionStorage.token || localStorage.token;
var E = window.wangEditor;
var editor = new E('#new_detail');

    // 隐藏“网络图片”tab
    editor.customConfig.showLinkImg = false;
    editor.customConfig.uploadImgServer = host+'/news/image_upload/'; // 上传图片到服务器
    // 隐藏“网络图片”tab
    editor.customConfig.showLinkImg = true;

    //限制图片大小为3M
    editor.customConfig.uploadImgMaxSize = 3 * 1024 * 1024;

    //限制图片上传数量
    editor.customConfig.uploadImgMaxLength = 6;

    // 上传图片时，可自定义filename，即在使用formdata.append(name, file)添加图片文件时，自定义第一个参数。

    editor.customConfig.uploadFileName = "new_image";
   //上传图片时刻自定义设置 header
    editor.customConfig.uploadImgHeaders = {
    "Authorization": "JWT " + token
    };
    //跨域上传中如果需要传递 cookie 需设置 withCredentials
    editor.customConfig.withCredentials = true;

    //可使用监听函数在上传图片的不同阶段做相应处理
    editor.customConfig.uploadImgHooks = {

        fail: function (xhr, editor, result) {
        // 图片上传并返回结果，但图片插入错误时触发
        // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象，result 是服务器端返回的结果
            alert(result.errmsg);
    },
        timeout: function (xhr, editor){
        // 图片上传超时时触发
        // xhr 是 XMLHttpRequst 对象，editor 是编辑器对象
    },
        // 如果服务器端返回的不是 {errno:0, data: [...]} 这种格式，可使用该配置
    // （但是，服务器端返回的必须是一个 JSON 格式字符串！！！否则会报错）
    customInsert: function (insertImg, result, editor) {
        // 图片上传并返回结果，自定义插入图片的事件（而不是编辑器自动插入图片！！！）
        // insertImg 是插入图片的函数，editor 是编辑器对象，result 是服务器端返回的结果

        // 举例：假如上传图片成功后，服务器端返回的是 {url:'....'} 这种格式，即可这样插入图片：
        var url = result.url;
        insertImg(url);

        // result 必须是一个 JSON 格式字符串！！！否则报错
    }


    };

//新闻分类
function newupload_category() {
    $.ajax({
        url:host+"/news/category/",

        type:"get",
        headers: {
                "Authorization": "JWT " + token
            },
        contentType:"application/json"

    }).done(function (resp) {
            if(resp.errmsg="OK") {
                for (var i = 0; i < resp.data.length; i++) {
                    var news_category = resp.data[i];

                    content = "<option value=" + news_category.id + ">" + news_category.name + "</option>";
                    $(".sel_opt").append(content)
                }
            }
    });
}

//获取查询字符串的值
function GetNewUpdate() {
    var url = location.search;
            //获取url中"?"符后的字串
    var theRequest = new Object();
        if (url.indexOf("?") != -1) {
            var str = url.substr(1);
            strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
            theRequest[strs[i].split("=")[0]]=decodeURI(strs[i].split("=")[1]);
            }
        }else {
            //如果没有查询字符串跳转到首页
            return false;
        }
        return theRequest;
    }


$(function(){

    //上传新闻分类显示
    newupload_category();

    //符文本编辑器创建
    editor.create();


    $(".news_edit").submit(function (e) {
        e.preventDefault();
        // TODO 新闻编辑提交

        //富文本新闻内容
        new_content = editor.txt.html();
        //防止xss攻击,过滤后的富文本内容
        filter_content = filterXSS(new_content);
        params = {
            "title":$(".input_txt2").val(),
            "category_id":$(".sel_opt").val(),
            "digest":$(".input_multxt").html(),
            "content":filter_content,
            "text":editor.txt.text()
        };

        $.ajax({
        url:host+"/news/upload/",
        data:JSON.stringify(params),
        type:"post",
         headers: {
                "Authorization": "JWT " + token
            },
        contentType:"application/json"

    }).done(function (resp) {

        alert("上传成功，正在审核中");
        location.reload();
        parent.location.reload();

        }).fail(function (resp) {
            alert(resp.errmsg);
        })


    });

    $(".news_update").submit(function (e) {
        e.preventDefault();
        // TODO 新闻编辑提交

        // 获取url中的new_id,获取不到new_id直接返回
        new_id = GetNewUpdate().new_id;
        // //富文本新闻内容
        // new_content = editor.txt.html();
        // //防止xss攻击,过滤后的富文本内容
        // filter_content = filterXSS(new_content);
        // params = {
        //     "title":$(".input_txt2").val(),
        //     "category_id":$(".sel_opt").val(),
        //     "digest":$(".input_multxt").html(),
        //     "content":filter_content,
        //     "text":editor.txt.text()
        // };
        $.ajax({
        url:host+"/news/"+new_id+"/update/",
        data:JSON.stringify(params),
        type:"post",
         headers: {
                "Authorization": "JWT " + token
            },
        contentType:"application/json"

    }).done(function (resp) {

        alert("修改成功，正在审核中");
        location.reload();
        parent.location.reload();

        }).fail(function (resp) {
            alert(resp.errmsg);
        })


    });
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1);
}