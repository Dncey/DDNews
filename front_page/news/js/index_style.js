
function change_banner(){
    $
}

$(function(){
    //判断是否登录,登录成功.user_info display:block, .setup disply:none;
    //页面滚动加载相关
    var flage=false
    $(window).scroll(function () {
        if(flage){
            $('.header1').hide();
        }
        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();
        if ( nowScroll > 140) {
            // TODO 判断页数，去更新新闻数据
            // alert('dsadsad');
            $('.header1').show();

            flage=true
        }
    })

    
    //菜单栏样式
    // $('.item').mouseover(function(){
    //     //添加类的类名不需要加.
    //     $(this).addClass('item_style')
    // }).mouseout(function(){
    //     $(this).removeClass('item_style')
    // });

    $('.item').click(function(){
            //添加类的类名不需要加.
            $('.item').removeClass('item_style')
            $(this).addClass('item_style');
            
        });
        
    //新闻图片悬浮放大
    $('.article_prc img').mouseover(function(){
        $(this).animate({'width':166,'height':166});
    }).mouseout(function(){
        $(this).animate({'width':161,'height':161});
    })

    // 轮播图
    var index = 0;
    var ago = 0;
    var t = setInterval(slide_show,3000);
    //默认静态播放的轮播图
    function slide_show(){
        //ago标记上一个索引
        ago = index;
        index++;
        if(index==3){
            index=0;
            ago = 2
        }
      
        $('.slide_item').eq(index).css({'display':'block'}).siblings('.slide_item').css({'display':'none'});
        //.不要忘加，圆点的轮播
        $('.item_radios').eq(ago).removeClass('active');
        $('.item_radios').eq(index).addClass('active');
        //上一个img直接消失，显示以动画的方式显示
        $('.slide_item').eq(ago).children('img').css({'opacity':0});
        $('.slide_item').eq(index).children('img').animate({opacity:1},700);  
    };

  // 应该点击轮播按钮时关闭定时器，然后切换各种样式，改变index然后在开始定时器
    $('.item_radios').click(function(){
        clearInterval(t);
        var radios_index = $(this).index();
        index = radios_index;
        $(this).addClass('active').siblings().removeClass('active');
        $('.slide_item').eq(index).css({'display':'block'}).siblings('.slide_item').css({'display':'none'});
        $('.slide_item').eq(index).children('img').css({'opacity':1});
        t = setInterval(slide_show,3000);
    });

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
        mask_flag=3;
    });
    $('.to_register').click(function(){
        $('.login_form_main').hide();
        $('.register_form_main').show();
        mask_flag=1;
    });
    $('.to_login').click(function(){
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
        }else if(mask_flag==3){
            $('.forget_form_main').hide();
        }else{
            $('.register_form_main').hide();
            $('.login_form_main').hide();
            
            $('.mask').hide();
        };    
    });

     //表单信息检验和错误信息的提示
 function error_message(errors){
    var error_div = '<div class="error_msg_inner">'+errors+'</div>'
        $('.error_msg').html(error_div);
        // $('.register_form_main').css({'height':553});
}

// var phone_num = $("input[name=register_phone_num]").val();
// //匹配手机号的正则
// var phone_Rex = /^1[3-9]\d{9}$/;
// var check_code = $("input[name=input_checkcode]").val();
// var phone_ckcode = $("input[name=phone_numbercode]").val();
// var password = $("input[name=userpassword]").val();
// var conpassword = $("input[name=confirm_password]").val();

    // $('.register_form').submit(function(event){
    //     // 阻止表单往action提交
    //     event.preventDefault();
        
    //     //判断各输入框是否为空
    //     if(!(phone_num&&check_code&&phone_ckcode&&password&&conpassword)){
    //         var ers='输入框有空,请仔细填写';
    //         error_message(ers);
    //         return
    //     }
    //     //判断手机号是否规范
    //     if(!phone_Rex.test(phone_num)){
    //         var ers='您输入的手机号有误!';
    //         error_message(ers);
    //         return
    //     }  
    //     //密码是否大于6位
    //     if(password.length<6){
    //         var ers='您输入密码长度小于6位!';
    //         error_message(ers);
    //         return
    //     }

    //     //两次密码是否出入正确
    //     if(password != conpassword){
    //         var ers='两次输入的密码不同!';
    //         error_message(ers);
    //         return
    //         }


        
    // });
    // // 发送手机短信验证码
    // $('.btn_get_checkcode').click(function(){
    //     //判断手机号是否规范
    //     if(!phone_Rex.test(phone_num)){
    //         var ers='您输入的手机号有误!';
    //         error_message(ers);
    //         return
    //     };

    //     var data = {
    //         'phone_num':phone_num,
    //         'check_code':check_code,
    //     }
    //     $.ajax({
    //         type: "post",
    //         url: "url",
    //         data: JSON.stringify(data),
    //         ContentType: "application/json",
    //         success: function (resp) {
    //             if(resp.data=='0'){

    //             }else{
    //                 alert(resp.data)
    //             }
    //         }
    //     });

    // })

   
    // $('.login_form_main').click(function(){
    //     return false;
    // })
    // 忘记密码
    

    // 搜索下拉框点击搜索框显示，点击其他任意地方隐藏，用到了事件冒泡阻止，
    $('.search_box').click(function(e){
        // return false;
        e.stopPropagation();
        $('.suggestion').show();
        $('.items').click(function(e){
            e.stopPropagation();
            var zz = $(this).children('.item_content').children().html();
            $('.search_input').val(zz);
            $('.suggestion').hide();
            //TODO
            $.get('/search.html',{title:zz}, function(resp){
                if(resp.errno=='0'){
                }
            });
            
        });
    });
    $('body').click(function(e){
        // return false;
        // e.stopPropagation();
        $('.suggestion').hide();
    });

   

    $('.btn_search').click(function(){

        $.get('/search.html/',)
    })

})