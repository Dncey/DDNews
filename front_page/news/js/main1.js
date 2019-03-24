var imageCodeId = ""; 
//匹配手机号的正则
var phone_Rex = /^1[3-9]\d{9}$/;
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
    $('.error_msg').html('');
var error_div = '<div class="error_msg_inner">'+errors+'</div>'
    $('.error_msg').html(error_div);
    // $('.register_form_main').css({'height':553});
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

    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {

        var r = (d + Math.random()*16)%16 | 0;

        d = Math.floor(d/16);

        return (c=='x' ? r : (r&0x3|0x8)).toString(16);

    });

    return uuid;

}

// 1.1 生成图片验证码

function generateImageCode() {

    imageCodeId = generateUUID();

    var ImageCodeID = '/img_code?code_id='+imageCodeId;

    $('.img_checkcode').attr('src',ImageCodeID);

};


// 退出按钮
function logout() {
    $.ajax({
        url: "/passport/logout",
        type: "post",
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function (resp) {
            // 刷新当前界面
            location.reload()
        }
    })
}



$(function(){

     //登录后鼠标移到个人头像位置，产生下拉框
     $('.user_info,.user_info_menu').mouseover(function(){
        $('.user_info_menu').css({'display':'block'});
    }).mouseout(function(){
        $('.user_info_menu').css({'display':'none'});
    })

     // 注册表单和登录表单的实现
    // 1为register,2为login,根据不同显示不同表单
    var mask_flag = 0
    $('.register_btn').click(function(){
        $('.register_form_main').show();
        $('.mask').show();
        mask_flag=1;
    });
    $('.shutoff').click(function(){
        $(this).parent().parent().hide();
         // 清空错误消息提示
         $('.error_msg').html('');
        $('.mask').hide();
    });
    $('.login_btn').click(function(){
        $('.login_form_main').show();
        $('.mask').show();
        mask_flag=2;
    });
    $('.forget_passwd a').click(function(){
        $('.login_form_main').hide();
        $('.forget_form_main').show();
         // 清空错误消息提示
         $('.error_msg').html('');
        mask_flag=3;
    });
    $('.to_register').click(function(){
        $('.login_form_main').hide();
        $('.register_form_main').show();
         // 清空错误消息提示
         $('.error_msg').html('');
        mask_flag=1;
    });
    $('.to_login').click(function(){
         // 清空错误消息提示
         $('.error_msg').html('');
        $('.register_form_main').hide();
        $('.forget_form_main').hide();
        $('.login_form_main').show();
        mask_flag=2;
    });
    $('.mask').click(function(){
        $(this).hide();
        if(mask_flag ==1){
            $('.register_form_main').hide();
            
        }else if(mask_flag==2){
            $('.login_form_main').hide();
             // 清空错误消息提示
            $('.error_msg').html('');
        }else if(mask_flag==3){
            $('.forget_form_main').hide();
             // 清空错误消息提示
            $('.error_msg').html('');
        }else{
            $('.register_form_main').hide();
            $('.login_form_main').hide();
             // 清空错误消息提示
            $('.error_msg').html('');
            
            $('.mask').hide();
        };    
    });
    
    

    // TODO 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    //获取图片验证码
    $('.register_btn,.forget_passwd a,.to_register').click(function(){
        generateImageCode();
    })
    


    
    // 1.2获取短信验证码
    //注册
    var flag=false
    $('.btn_get_checkcode ').click(function() {
        if (flag){
            var ers='请等待倒计时结束!';
            error_message(ers);
            return;
        }
        // 图片验证码
        var check_code = $(".input_code").val();
        // 手机号
        var phone_num = $(".phonenum").val();

        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers='手机号不正确!';
            error_message(ers);
            return
        };

        if (!check_code) {

            var ers='图片验证码不能为空!';
            error_message(ers);
            return

        }
        // 清空错误消息提示
        $('.error_msg').html('');
    
        // TODO 发送短信验证码

        params ={

            'mobile':phone_num,

            'imageCode':check_code,

            'imageCodeId':imageCodeId

        };

        $.ajax({

            url:'/passport/sendSMSCode/',

            type:'post',

            headers:{

                "X-CSRFToken": getCookie("csrf_token")

            },

            data:JSON.stringify(params),

            contentType:'application/json',

            success:function (resp) {

                if(resp.errno=='0'){
                    var time = 60;
        
                    var t = setInterval(function () {
                        
                        if(time==1){
            
                            clearInterval(t);
                            
                            $(".btn_get_checkcode").html('点击获取验证码');
                            $('.error_msg').html('');
                            flag=false;
            
                        }else {
                            
                            flag = true
                            
                            time -=1;
            
                            $('.btn_get_checkcode').html(time+'秒');    
                        }
                            },1000)
            
                

                }else {

                    alert(resp.errmsg);
                }

            }

        })

    })
    var flags =false
    //忘记密码获取短信验证码
    $('.btn_checkcode ').click(function() {
        if (flags){
            var ers='请等待倒计时结束!';
            error_message(ers);
            return;
        }
        // 图片验证码
        var check_code = $(".forget_form .input_code").val();
        // 手机号
        var phone_num = $(".forget_form .phonenum").val();

        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers='手机号不正确!';
            error_message(ers);
            return
        };

        if (!check_code) {

            var ers='图片验证码不能为空!';
            error_message(ers);
            return

        }
        // 清空错误消息提示
        $('.error_msg').html('');

        // TODO 发送短信验证码

        params ={

            'mobile':phone_num,

            'imageCode':check_code,

            'imageCodeId':imageCodeId

        };

        $.ajax({

            url:'/passport/sendSMSCode/',

            type:'post',

            headers:{

                "X-CSRFToken": getCookie("csrf_token")

            },

            data:JSON.stringify(params),

            contentType:'application/json',

            success:function (resp) {

                if(resp.errno=='0'){

                    var time = 60;

                    var t = setInterval(function () {

                        if(time==1){

                            clearInterval(t);
                            flags=false;
                            // 清空错误消息提示
                            $('.error_msg').html('');
                            $(".btn_checkcode").html('点击获取验证码');


                        }else {
                            flags=true;
                            time -=1;
                            $('.btn_checkcode').html(time+'秒');
                        }

                    },1000)

                }else {

                    alert(resp.errmsg);

                }

            }

        })

    })

    //1.3 TODO 注册按钮点击
    $('.register_form').submit(function(event){
        // 阻止表单往action提交
        event.preventDefault();
        // 手机号
        var phone_num = $(".phonenum").val();
        // 短信验证码
        var phone_ckcode = $(".input_phonecode").val();

        // 密码
        var password = $(".password").val();
        // 确认密码
        var conpassword = $(".confirm_password").val();

        //判断各输入框是否为空
        if(!(phone_num&&phone_ckcode&&password&&conpassword)){
            var ers='输入框有空,请仔细填写';
            error_message(ers);
            return
        }
        //判断手机号是否规范
        if(!phone_Rex.test(phone_num)){
            var ers='您输入的手机号有误!';
            error_message(ers);
            return
        }  
        //密码是否大于6位
        if(password.length<6){
            var ers='您输入密码长度小于6位!';
            error_message(ers);
            return
        }

        //两次密码是否出入正确
        if(password != conpassword){
            var ers='两次输入的密码不同!';
            error_message(ers);
            return
            }

         // 清空错误消息提示
        $('.error_msg').html('');
        params = {
        'mobile':phone_num,

        'sms_code':phone_ckcode,

        'password':password};

        // 发起注册请求

            $.ajax({

                url:'/passport/register',

                type:'post',

                headers:{

                    "X-CSRFToken": getCookie("csrf_token")

                },

                data:JSON.stringify(params),

                contentType:'application/json',

                success:function (resp) {

                    if(resp.errno=='0'){

                        location.reload();

                    }else {
                        error_message(resp.errmsg);
                    }

                }

        })      
    });


    // 1.4登录

    $(".login_form").submit(function (e) {
        e.preventDefault();

        // 手机号/用户名/邮箱
        var lgoin_text = $(".lgoin_text").val();
        // 密码
        var password = $(".password").val();


         //判断各输入框是否为空
         if(!(lgoin_text&&password)){
            var ers='输入框有空,请仔细填写';
            error_message(ers);
            return
        }
        //密码是否大于6位
        if(password.length<6){
            var ers='您输入密码长度小于6位!';
            error_message(ers);
            return
        }
        // 清空错误消息提示
        $('.error_msg').html('');

        // 发起登录请求

        params = {

            'lgoin_text':lgoin_text,

            'password':password

        }

        $.ajax({

            url:'/passport/login',

            type:'post',

            headers:{

                "X-CSRFToken": getCookie("csrf_token")

            },

            data:JSON.stringify(params),

            contentType:'application/json',

            success:function (resp) {

                if(resp.errno == '0'){

                    location.reload()

                }else {

                    alert(resp.errmsg)

                }

            }



        })

    })

    // 1.5忘记密码


    $('.forget_form').submit(function(e){
        e.preventDefault();

        // 短信验证码
        var phone_ckcode = $(".input_phonecode").val();
        // 手机号
        var phonenum = $(".phonenum").val();
        // 密码
        var password = $(".password").val();
        //判断各输入框是否为空
        if(!(phonenum&&phone_ckcode&&password)){
            var ers='输入框有空,请仔细填写';
            error_message(ers);
            return
        }
        //判断手机号是否规范
        if(!phone_Rex.test(phonenum)){
            var ers='您输入的手机号有误!';
            error_message(ers);
            return
        }  
        //密码是否大于6位
        if(password.length<6){
            var ers='您输入密码长度小于6位!';
            error_message(ers);
            return
        }
         // 清空错误消息提示
         $('.error_msg').html('');
        params = {

            'mobile':phonenum,
            
            'smscode':phone_ckcode,

            'password':password

        }

        $.ajax({

            url:'/passport/resetpwd/',

            type:'post',

            headers:{

                "X-CSRFToken": getCookie("csrf_token")

            },

            data:JSON.stringify(params),

            contentType:'application/json',

            success:function (resp) {

                if(resp.errno == '0'){

                    location.reload()

                }else {

                    alert(resp.errmsg)

                }

            }



        })





    })
    
    //搜索小图标效果
    $('.search_icon').click(function(){
        
    })

});


    // ---------------------------------------------


	


	







	// 根据地址栏的hash值来显示用户中心对应的菜单

	// var sHash = window.location.hash;

	// if(sHash!=''){

	// 	var sId = sHash.substring(1);

	// 	var oNow = $('.'+sId);		

	// 	var iNowIndex = oNow.index();

	// 	$('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');

	// 	oNow.show().siblings().hide();

	// }



	// 用户中心菜单切换

	// var $li = $('.option_list li');

	// var $frame = $('#main_frame');



	// $li.click(function(){

	// 	if($(this).index()==5){

	// 		$('#main_frame').css({'height':900});

	// 	}

	// 	else{

	// 		$('#main_frame').css({'height':660});

	// 	}

	// 	$(this).addClass('active').siblings().removeClass('active');

	// 	$(this).find('a')[0].click()

	// })



    


















// 调用该函数模拟点击左侧按钮

function fnChangeMenu(n) {

    var $li = $('.option_list li');

    if (n >= 0) {

        $li.eq(n).addClass('active').siblings().removeClass('active');

        // 执行 a 标签的点击事件

        $li.eq(n).find('a')[0].click()

    }

}



// 一般页面的iframe的高度是660

// 新闻发布页面iframe的高度是900

function fnSetIframeHeight(num){

	var $frame = $('#main_frame');

	$frame.css({'height':num});

}







// function logout() {

//     $.get('/logout',function (resp) {

//         location.reload();

//     })
// }
