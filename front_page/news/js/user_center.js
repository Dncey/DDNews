/**
 * Created by python on 19-4-30.
 */


$(function () {
    //获取分类信息
    getCategoryinfo();

    //判断用户是否登录
    if( !judge_user()){
        alert("请登录后今日个人中心");
        location.href="/";
    }
    //根据用户点击菜单添加效果事件

    $(".option_list li").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
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

    $("body").click(function(e){
        // return false;
        // e.stopPropagation();
        $(".suggestion").hide();
    });
});