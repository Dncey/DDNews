

//获取查询字符串的值
function GetRequest() {
    var url = location.search;
            //获取url中"?"符后的字串
    var theRequest = new Object();
        if (url.indexOf("?") != -1) {
            var str = url.substr(1);
            strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
            theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
            }
        }else {
            //如果没有查询字符串跳转到首页
            return location.href="/";
        }
        return theRequest;
    }

//获取详情页新闻信息
function GetDetailNew() {
    var data = GetRequest();
    if(data["new_id"]){
        var new_id = data["new_id"];

         $.ajax({
        url:host+"/news/detail/"+ new_id+"/",
        type: "GET",
        ContentType:"application/json"
        }).done(function (resp) {

            var new_title = resp.title.replace("今日头条"," ");
            $(".news_content >h2").html(new_title);
            $(".time_source").html(resp.report_time+" 来源:"+resp.source);

            //替换今日头条
            var new_content = resp.content.replace("今日头条"," ");
            $(".new_content").html(new_content);
            if(resp.user.avatar_url){
                $(".author_icon").attr("src",resp.user.avatar_url)
            }
            $(".author_icon").attr("href","/author_center.html?author_id="+resp.user.id);
            $(".author_nickname").attr("href","/author_center.html?author_id="+resp.user.id).html(resp.user.username);
            $(".right_top >p").html(resp.user.signature);



         }).fail(function (resp) {
             console.log("hello");
         })
    }else {
        location.href="/" ;
    }

}

//获取当前用户是否关注该作者
function GetFollow() {
    $.ajax({
        url:host+"/user/author/"+GetRequest().new_id+"/followed/",
        type: "get",
        headers:{
            "Authorization": "JWT " + token
        },
        ContentType:"application/json"
    }).done(function (resp) {
        console.log("zz")
    }).fail(function (resp) {
        console.log("mm")
    })
}
//获取收藏信息
function GetCollected() {
    params = {
        "new_id":GetRequest()
    };
     $.ajax({
        url:host+"/new/collected/",
        type: "post",
        data:JSON.stringify(params),
        headers:{
            "Authorization": "Bearer " + token
        },
        ContentType:"application/json"
    });
}


$(function () {

    GetDetailNew();

    GetFollow();

     //判断用户是否登录
    if(judge_user()){
    //    发送请求判断该用户是否关注该作者
    }else {
    //   将关注显示
        $(".unfocus").css({"display":"none"});
    }




    //获取分类信息
    getCategoryinfo();


});