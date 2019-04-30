
// function change_banner(){
//
// }

$(function(){
    //判断是否登录,登录成功.user_info display:block, .setup disply:none;
    //页面滚动加载相关
    var flage=false;
    $(window).scroll(function () {
        if(flage){
            $(".header1").hide();
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
            //  判断页数，去更新新闻数据
            // alert("dsadsad");
            $(".header1").show();

            flage=true;
        }
    });
    //菜单栏样式
    // $(".item").mouseover(function(){
    //     //添加类的类名不需要加.
    //     $(this).addClass("item_style")
    // }).mouseout(function(){
    //     $(this).removeClass("item_style")
    // });

    $(".item").click(function(){
            //添加类的类名不需要加.
            $(".item").removeClass("item_style");
            $(this).addClass("item_style");
        });
    //新闻图片悬浮放大
    $(".article_prc > img").mouseover(function(){
        $(this).animate({"width":160,"height":100});
    }).mouseout(function(){
        $(this).animate({"width":150});
    });

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
            ago = 2;
        }
        $(".slide_item").eq(index).css({"display":"block"}).siblings(".slide_item").css({"display":"none"});
        //.不要忘加，圆点的轮播
        $(".item_radios").eq(ago).removeClass("active");
        $(".item_radios").eq(index).addClass("active");
        //上一个img直接消失，显示以动画的方式显示
        $(".slide_item").eq(ago).children("img").css({"opacity":0});
        $(".slide_item").eq(index).children("img").animate({opacity:1},700);
    }

  // 应该点击轮播按钮时关闭定时器，然后切换各种样式，改变index然后在开始定时器
    $(".item_radios").click(function(){
        clearInterval(t);
        var radios_index = $(this).index();
        index = radios_index;
        $(this).addClass("active").siblings().removeClass("active");
        $(".slide_item").eq(index).css({"display":"block"}).siblings(".slide_item").css({"display":"none"});
        $(".slide_item").eq(index).children("img").css({"opacity":1});
        t = setInterval(slide_show,3000);
    });

     //表单信息检验和错误信息的提示
 function error_message(errors){
    var error_div = "<div class='error_msg_inner'>"+errors+"</div>";
        $(".error_msg").html(error_div);
        // $(".register_form_main").css({"height":553});
}
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


    $("body").click(function(e){
        // return false;
        // e.stopPropagation();
        $(".suggestion").hide();
    });


});