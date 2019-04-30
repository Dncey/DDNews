var imageCodeId = "";
//匹配手机号的正则
var phone_Rex = /^1[3-9]\d{9}$/;




var username = sessionStorage.username || localStorage.username;
var user_id = sessionStorage.user_id || localStorage.user_id;
var token = sessionStorage.token || localStorage.token;
var avatar_url = sessionStorage.avatar_url || localStorage.avatar_url;
// // 图片验证码
// var check_code = $(".input_code").val();

// // 短信验证码
// var phone_ckcode = $(".input_phonecode").val();
// // 手机号
// var phone_num = $(".phonenum").val();
// // 密码
// var password = $(".password").val();
// // 确认密码
// var conpassword = $(".confirm_password").val();

//表单信息检验和错误信息的提示
function error_message(errors){
    $(".error_msg").html("");
var error_div = "<div class='error_msg_inner'>"+errors+"</div>";
    $(".error_msg").html(error_div);
    // $(".register_form_main").css({"height":553});
}


function getCookie(name) {

    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");

    return r ? r[1] : undefined;

}

function generateUUID() {

    var d = new Date().getTime();

    if(window.performance && typeof window.performance.now === "function"){

        d += performance.now(); //use high-precision timer if available

    }

    var uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {

        var r = (d + Math.random()*16)%16 | 0;

        d = Math.floor(d/16);

        return (c=="x" ? r : (r&0x3|0x8)).toString(16);

    });

    return uuid;

}

//获取分类信息
function getCategoryinfo() {
    $.ajax({
        url:host+"/news/category/",

        type:"get",

        contentType:"application/json"

    }).done(function (resp) {
            if(resp.errmsg="OK"){
                for(var i =0;i<resp.data.length;i++){
                    var news_category = resp.data[i];
                    //如果分类的长度大于三一个样式
                    if(news_category.name.length>=3){
                        content = "<a class='item three' category_id='"+news_category.id+"'>";
                        content1 = "<a href='index.html?category_id="+news_category.id+"' class='item three' category_id='"+news_category.id+"'>";
                    }
                    else {
                       content = "<a class='item' category_id='"+news_category.id+"'>";
                    content1 = "<a href='index.html?category_id="+news_category.id+"' class='item' category_id='"+news_category.id+"'>";
                    }
                    content +=news_category.name +"</a>";
                    content1 +=news_category.name +"</a>";
                    $(".list").append(content);
                    $(".categroy").append(content1);
                }
        $(".list").append("<span class='more_item'>更多</span>");
            }
        //从其他页跳转到主页,携带的分类参数;
       if(index_GetRequest().category_id){
            $(".item[category_id="+index_GetRequest().category_id+"]").click();
            // $(".item[category_id='2']").click();
    }
    })
}



// 1.1 生成图片验证码

function generateImageCode() {

    imageCodeId = generateUUID();

    var ImageCodeID = host+"/passport/img_code/"+imageCodeId+"/";

    $(".img_checkcode").attr("src",ImageCodeID);

}


// 退出按钮
function logout() {
    sessionStorage.clear();
    localStorage.clear();
    location.reload();
}

//获取搜索关键字

//获取搜索热度关键字
function getSearchKeys() {
    $.ajax({
        url:host+"/news/keysword/",

        type:"get",

        contentType:"application/json"

    }).done(function (resp) {
            if(resp.errmsg="OK"){
                for(var i =0;i<resp.data.length;i++){
                    var search_keys = resp.data[i];
                    //如果分类的长度大于三一个样式
                    content = " <a class='items item_"+(i+1)+"'>";
                    if(i<3){
                        content +=" <div class=' index icon_"+(i+1)+"'>"+ (i+1)+"</div>"
                    }else {
                        content +="  <div class='index  icon'>"+(i+1)+"</div>"
                    }
                    content += " <div class='item_content'> <div class='hot_search_word'>"+search_keys+"</div> </div> </a>";
                    $(".inner_block_box").append(content)
                }
            }else {
                alert("获取数据错误");
            }
        })
}

//发送jwt判断有效期
function judge_jwt() {
    $.ajax({
        url:host+"/judge_jwt/",
        type:"post",
        data:JSON.stringify({
            "token":token
        }),
        contentType:"application/json"
    }).done(function () {
        return true;
    }).fail(function(){
        sessionStorage.clear();
        localStorage.clear();
        return false;
    })
}

//判断用户登录状态设置样式
function judge_user() {
    if(! avatar_url){
        avatar_url = "img/person.jpeg";
    }

    if(username&&user_id&&token){
        $(".setup").css({"display":"none"});
        $(".user_info").css({"display":"block"});
        $(".header1_login").css({"display":"none"});
        $(".header1 .user_info").css({"display":"block"});
        //更换用户头像
        $(".info_icon").attr("src",avatar_url);
        $(".info_name").html(username);
        //更换用户中心的头像和用户名
        $(".user_center_pic img").attr("src",avatar_url,"alt",username);
        $(".user_center_name").html(username);

        $(".user_center").attr("href","user.html?user_id="+user_id);
        return true;

    }else {
        $(".setup").css({"display":"block"});
        $(".user_info").css({"display":"none"});
        $(".header1_login").css({"display":"block"});
        $(".header1 .user_info").css({"display":"none"});
        return false;
    }


}


//获取查询字符串的值
function GetRequest() {
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
            return location.href="/";
        }
        return theRequest;
    }

//关注的鼠标移入移除样式
function FocusStyle() {
    $(".unfocus").mouseover(function () {
        $(".unfocus > .out").css({"display":"none"});
        $(".unfocus > .over").css({"display":"block"});
    }).mouseout(function () {
        $(".unfocus > .out").css({"display":"block"});
        $(".unfocus > .over").css({"display":"none"});
    })
}


//主页获取查询字符串(分类id)的值
function index_GetRequest() {
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
            return
        }
        return theRequest;
    }




$(function(){



    //判断jwt是否过期
    judge_jwt();

    // 获取搜索热度关键字
    getSearchKeys();

     //判断用户是否登录
    judge_user();
     //搜索关键字跳转
    $(".btn_search").click(function () {
        var text = $(".search_input").val();
        if(!text){
            alert("搜索内容不能为空");
            return;
        }
        location.href = "search.html?search_keywords="+text;
    });


    // 搜索下拉框点击搜索框显示，点击其他任意地方隐藏，用到了事件冒泡阻止，
    $(".search_box").click(function(e){
        // return false;
        e.stopPropagation();
        $(this).children(".suggestion").show();
        // $(".suggestion").show();
        $(".items").click(function(e){
            e.stopPropagation();
            var zz = $(this).children(".item_content").children().html();
            $(".search_input").val(zz);
            $(".suggestion").hide();
            //need do
            $.get("/search.html",{title:zz}, function(resp){
                if(resp.errno=="0"){
                }
            });
        });
    });



     //登录后鼠标移到个人头像位置，产生下拉框
     $(".user_info,.user_info_menu").mouseover(function(){
        $(".user_info_menu").css({"display":"block"});
    }).mouseout(function(){
        $(".user_info_menu").css({"display":"none"});
    });

     // 注册表单和登录表单的实现
    // 1为register,2为login,根据不同显示不同表单
    var mask_flag = 0;
    $(".register_btn").click(function(){
        $(".register_form_main").show();
        $(".mask").show();
        mask_flag=1;
    });
    $(".shutoff").click(function(){
        $(this).parent().parent().hide();
         // 清空错误消息提示
         $(".error_msg").html("");
        $(".mask").hide();
    });
    $(".login_btn").click(function(){
        $(".login_form_main").show();
        $(".mask").show();
        mask_flag=2;
    });
    $(".forget_passwd a").click(function(){
        $(".login_form_main").hide();
        $(".forget_form_main").show();
         // 清空错误消息提示
         $(".error_msg").html("");
        mask_flag=3;
    });
    $(".to_register").click(function(){
        $(".login_form_main").hide();
        $(".register_form_main").show();
         // 清空错误消息提示
         $(".error_msg").html("");
        mask_flag=1;
    });
    $(".to_login").click(function(){
         // 清空错误消息提示
         $(".error_msg").html("");
        $(".register_form_main").hide();
        $(".forget_form_main").hide();
        $(".login_form_main").show();
        mask_flag=2;
    });
    $(".mask").click(function(){
        $(this).hide();
        if(mask_flag ==1){
            $(".register_form_main").hide();
        }else if(mask_flag==2){
            $(".login_form_main").hide();
             // 清空错误消息提示
            $(".error_msg").html("");
        }else if(mask_flag==3){
            $(".forget_form_main").hide();
             // 清空错误消息提示
            $(".error_msg").html("");
        }else{
            $(".register_form_main").hide();
            $(".login_form_main").hide();
             // 清空错误消息提示
            $(".error_msg").html("");
            $(".mask").hide();
        }
    });

    // TODO 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    //获取图片验证码
    $(".register_btn,.forget_passwd a,.to_register").click(function(){
        generateImageCode();
    });
    $(".imgcode").click(function () {
        generateImageCode();
    });
    // 1.2获取短信验证码
    //注册
    var flag=false;
    $(".btn_get_checkcode ").click(function() {
        if (flag){
            var ers="请等待倒计时结束!";
            error_message(ers);
            return;
        }
        // 图片验证码
        var check_code = $(".input_code").val();
        // 手机号
        var phone_num = $(".phonenum").val();

        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers="手机号不正确!";
            error_message(ers);
            return
        }

        if (!check_code) {

            var ers="图片验证码不能为空!";
            error_message(ers);
            return

        }
        // 清空错误消息提示
        $(".error_msg").html("");
        // TODO 发送短信验证码

        params ={

            "mobile":phone_num,

            "imageCode":check_code,

            "imageCodeId":imageCodeId

        };

        $.ajax({

            url:host +"/passport/sendSMSCode/register/",

            type:"post",

            data:JSON.stringify(params),

            contentType:"application/json",

            success:function (resp) {

                if(resp.errmsg=="OK"){
                    var time = 60;
                    var t = setInterval(function () {
                        if(time==1){
                            clearInterval(t);
                            $(".btn_get_checkcode").html("点击获取验证码");
                            $(".error_msg").html("");
                            flag=false;}else {
                            flag = true;
                            time -=1;
                            $(".btn_get_checkcode").html(time+"秒");
                        }
                            },1000)

                }else {

                    error_message(resp.errmsg);
                }

            }

        })

    });


    var flags =false;
    //忘记密码获取短信验证码
    $(".btn_checkcode ").click(function() {
        if (flags){
            var ers="请等待倒计时结束!";
            error_message(ers);
            return;
        }
        // 图片验证码
        var check_code = $(".forget_form .input_code").val();
        // 手机号
        var phone_num = $(".forget_form .phonenum").val();

        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers="手机号不正确!";
            error_message(ers);
            return
        }

        if (!check_code) {

            var ers="图片验证码不能为空!";
            error_message(ers);
            return

        }
        // 清空错误消息提示
        $(".error_msg").html("");

        // TODO 发送短信验证码

        params ={

            "mobile":phone_num,

            "imageCode":check_code,

            "imageCodeId":imageCodeId

        };

        $.ajax({

            url:host+"/passport/sendSMSCode/forget/",

            type:"post",

            data:JSON.stringify(params),

            contentType:"application/json",

            success:function (resp) {

                if(resp.errmsg=="OK"){

                    var time = 60;

                    var t = setInterval(function () {

                        if(time==1){

                            clearInterval(t);
                            flags=false;
                            // 清空错误消息提示
                            $(".error_msg").html("");
                            $(".btn_checkcode").html("点击获取验证码");


                        }else {
                            flags=true;
                            time -=1;
                            $(".btn_checkcode").html(time+"秒");
                        }

                    },1000)

                }else {

                     error_message(resp.errmsg);

                }

            }

        })

    });


    //1.3 TODO 注册按钮点击
    $(".register_form").submit(function(event){
        // 阻止表单往action提交
        event.preventDefault();
        // 手机号
        var phone_num = $(".phonenum").val();
        // 短信验证码
        var phone_ckcode = $(".input_phonecode").val();

        // 密码
        var password = $(".register_password").val();
        // 确认密码
        var conpassword = $(".confirmed_password").val();
        //　是否遵循协议
        var is_checker = $("#agree_check").is(":checked");
        //判断各输入框是否为空
        if(!(phone_num&&phone_ckcode&&password&&conpassword)){
            var ers="输入框有空,请仔细填写";
            error_message(ers);
            return
        }
        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers="您输入的手机号有误!";
            error_message(ers);
            return
        }
        //密码是否大于6位
        if(password.length<6){
            var ers="您输入密码长度小于6位!";
            error_message(ers);
            return
        }

        //两次密码是否出入正确
        if(password != conpassword){
            var ers="两次输入的密码不同!";
            error_message(ers);
            return
            }

         // 清空错误消息提示
        $(".error_msg").html("");
        params = {
        "mobile":phone_num,
        "sms_code":phone_ckcode,
        "password":password,
        "is_checked":is_checker,
        "confirm_pwd":conpassword
        };

        // 发起注册请求

            $.ajax({

                url:host+"/passport/register/",

                type:"post",

                data:JSON.stringify(params),

                contentType:"application/json",

                success:function (resp) {

                    if(resp.errmsg=="OK"){

                         // 记录用户的登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage["token"] = resp.data.token;
                        localStorage["username"] = resp.data.username;
                        localStorage["user_id"] = resp.data.user_id;
                        localStorage["avatar_url"] = resp.data.avatar_url;
                        location.reload();
                    }else {
                        error_message(resp.errmsg);
                    }

                }

        });
    });


    // 1.4登录

    $(".login_form").submit(function (e) {
        e.preventDefault();

        // 手机号/用户名/邮箱
        var lgoin_text = $(".lgoin_text").val();
        // 密码
        var password = $(".password").val();
         //是否记住登录状态
        var remuser = $("#agree_check").is(":checked");

         //判断各输入框是否为空
         if(!(lgoin_text&&password)){
            var ers="输入框有空,请仔细填写";
            error_message(ers);
            return
        }
        //密码是否大于6位
        if(password.length<6){
            var ers="您输入密码长度小于6位!";
            error_message(ers);
            return
        }
        // 清空错误消息提示
        $(".error_msg").html("");

        // 发起登录请求

        params = {

            "login_text":lgoin_text,

            "password":password

        };

        $.ajax({

            url:host+"/passport/login/",

            type:"post",

            data:JSON.stringify(params),

            contentType:"application/json",

            success:function (resp) {

                if(resp.errmsg == "OK"){
                    //如果记住user信息存在localStorage中,否则存储到sessionStorage中
                    if(remuser){
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage.token = resp.data.token;
                        localStorage.user_id = resp.data.user_id;
                        localStorage.username = resp.data.username;
                        localStorage.avatar_url = resp.data.avatar_url
                    }else {
                        localStorage.clear();
                        sessionStorage.clear();
                     　　sessionStorage.token = resp.data.token;
                        sessionStorage.user_id = resp.data.user_id;
                        sessionStorage.username = resp.data.username;
                        sessionStorage.avatar_url = resp.data.avatar_url
                    }
                    location.reload();

                }else {

                    error_message(resp.errmsg);

                }

            }



        })

    });

    // 1.5忘记密码

    $(".forget_form").submit(function(e){
        e.preventDefault();

        // 短信验证码
        var phone_ckcode = $(".input_phonecodetext >.sms_code").val();
        // 手机号
        var phonenum = $(".forget_form >.phonenum").val();
        // 密码
        var password = $(".forget_password").val();
        //判断各输入框是否为空
        if(!(phonenum&&phone_ckcode&&password)){
            var ers="输入框有空,请仔细填写";
            error_message(ers);
            return
        }
        //判断手机号是否规范
        if(!phone_Rex.test(phonenum)){
            var ers="您输入的手机号有误!";
            error_message(ers);
            return
        }
        //密码是否大于6位
        if(password.length<6){
            var ers="您输入密码长度小于6位!";
            error_message(ers);
            return
        }
         // 清空错误消息提示
         $(".error_msg").html("");
        params = {

            "mobile":phonenum,
            "smscode":phone_ckcode,
            "password":password

        };

        $.ajax({

            url:host+"/passport/resetpwd/",

            type:"post",

            data:JSON.stringify(params),

            contentType:"application/json",

            success:function (resp) {

                if(resp.errmsg == "OK"){
                    // 记录用户的登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage["token"] = resp.data.token;
                        localStorage["username"] = resp.data.username;
                        localStorage["user_id"] = resp.data.user_id;
                        localStorage["avatar_url"] = resp.data.avatar_url;
                        location.reload()

                }else {

                    error_message(resp.errmsg);

                }

            }



        })





    });



    //固定菜单栏搜索小图表点击

    $(document).on("click",".search_icon",function(e){

     var text = $(".header1 .search_box > input").val();
        if(!text){
            alert("搜索内容不能为空");
            return;
        }
        location.href = "search.html?search_keywords="+text;
    });


});


    // ---------------------------------------------









	// 根据地址栏的hash值来显示用户中心对应的菜单

	// var sHash = window.location.hash;

	// if(sHash!=""){

	// 	var sId = sHash.substring(1);

	// 	var oNow = $("."+sId);		

	// 	var iNowIndex = oNow.index();

	// 	$(".option_list li").eq(iNowIndex).addClass("active").siblings().removeClass("active");

	// 	oNow.show().siblings().hide();

	// }



	// 用户中心菜单切换

	// var $li = $(".option_list li");

	// var $frame = $("#main_frame");



	// $li.click(function(){

	// 	if($(this).index()==5){

	// 		$("#main_frame").css({"height":900});

	// 	}

	// 	else{

	// 		$("#main_frame").css({"height":660});

	// 	}

	// 	$(this).addClass("active").siblings().removeClass("active");

	// 	$(this).find("a")[0].click()

	// })



    


















// 调用该函数模拟点击左侧按钮

function fnChangeMenu(n) {

    var $li = $(".option_list li");

    if (n >= 0) {

        $li.eq(n).addClass("active").siblings().removeClass("active");

        // 执行 a 标签的点击事件

        $li.eq(n).find("a")[0].click()

    }

}



// 一般页面的iframe的高度是660

// 新闻发布页面iframe的高度是900

function fnSetIframeHeight(num){

	var $frame = $("#main_frame");

	$frame.css({"height":num});

}







// function logout() {

//     $.get("/logout",function (resp) {

//         location.reload();

//     })
// }
