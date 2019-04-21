
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var page_size = 10;

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
                $(".author_image_box").attr("src",resp.user.avatar_url)
            }
            $(".author_image_box").attr("href","author_center.html?author_id="+resp.user.id);
            $(".author_nickname").attr("href","author_center.html?author_id="+resp.user.id).html(resp.user.username);
            $(".right_top >p").html(resp.user.signature);

             $(".right_top").attr("author_id",resp.user.id);



         }).fail(function (resp) {
             console.log("hello");
         })
    }else {
        location.href="/" ;
    }

}


//获取收藏信息
function GetCollected() {
    params = {
        "new_id":GetRequest()
    };
     $.ajax({
        url:host+"/news/collected/",
        type: "post",
        data:JSON.stringify(params),
        headers:{
            "Authorization": "Bearer " + token
        },
        ContentType:"application/json"
    });
}

//发起关注请求
function Followed() {
    params = {
        author_id: $(".right_top").attr("author_id")
    };
    $.ajax({
        url:host+"/user/author/followed/",
        type: "post",
        headers:{
            "Authorization": "JWT " + token
        },
        data : params,

        ContentType:"application/json"
    }).done(function (resp) {
        if(resp.errmsg=="OK"){
            $(".unfocus").css({"display":"inline-block"});
            $(".focus").css({"display":"none"});
        }else {
            alert(resp.errmsg)
        }

    }).fail(function (resp) {
        alert(resp.responseJSON.errmsg);
    })
}

//获取当前用户是否关注该作者
function GetFollow() {
    $.ajax({
        url:host+"/user/author/"+GetRequest().new_id+"/follow/",
        type: "get",
        headers:{
            "Authorization": "JWT " + token
        },
        ContentType:"application/json"
    }).done(function (resp) {
        if(resp.data=="true"){
            $(".unfocus").css({"display":"inline-block"});
            $(".focus").css({"display":"none"});
        }else{
            $(".unfocus").css({"display":"none"});
        $(".focus").css({"display":"inline-block"});
        }
    }).fail(function (resp) {
        console.log("获取信息失败")

    })
}

//取消关注
function Remove_Follow() {
    params = {
        author_id: $(".right_top").attr("author_id")
    };
    $.ajax({
        url:host+"/user/author/followed/",
        type: "delete",
        headers:{
            "Authorization": "JWT " + token
        },
        data : params,

        ContentType:"application/json"
    }).done(function (resp) {
        if(resp.errmsg=="OK"){
            $(".unfocus").css({"display":"none"});
            $(".focus").css({"display":"inline-block"});
        }else {
            alert(resp.errmsg)
        }
});}



//发送评论(包含父和子)
function Add_comment(parent_id,comment) {
    params={
        parent_id:parent_id,
        content:comment,
        new_id:GetRequest().new_id
    };
    $.ajax({
        url:host+"/news/comment/",
        type: "post",
        headers:{
            "Authorization": "JWT " + token
        },
        data : params,

        ContentType:"application/json"
    }).done(function (resp) {
        if(parent_id=="null"){
        content = "<li data_id='"+resp.id+"'>";
        if(resp.user.avatar_url){
            content +="<img src='"+resp.user.avatar_url+"'>";
        }else{
            content +="<img src='img/person.jpeg'>";
        }
        content +="<div class='comment-box'> <span class='comment_nickname' user_id='"+resp.user.id+"'>"+resp.user.username+"</span>";
            content +="<span class='comment_date'>"+resp.create_time+"</span>";
                    content += "<a class='comment_report' href='javascript:;' data_id='"+resp.id+"' data-type='comment'>举报";
                    content += "</a><a href='javascript:;' class='comment_reply' replay_id='"+resp.id+"'>回复</a>";
                    content += "<a href='javascript:;' class='float-right comment_like '>"+resp.like +"赞</a>";
                    content += "</div> <p>"+resp.content+"</p></li>";
                    //添加到元素内部的前面
                    $(".comment_list").prepend(content);
                    $(".comment_input").val(" ");
        }else {
            content = "<div class='reply_list'>  <div data_id='"+resp.id+"'><a class='ft_blue can_reply' title='点击回复他' href='javascript:;'>"+resp.user.username+":</a>"+resp.content+"<a href='javascript:;' data_id='"+resp.id+"' class='comment_report' data-type='reply'>举报</a><a href='javascript:;' class='float-right comment_like '>"+resp.like +"赞</a> </div>  </div>";
            $("li[data_id="+parent_id+"]").append(content);

            //文本输入框隐藏
            $(".reply_input").remove();
            reply_input_flag = 0;
            console.log($("li[data_id=parent_id]"))
        }

}).fail(function (resp) {
        alert(resp.responseText);
    });
}


//孙子评论发送
function subs_Addcomment(parent_id,comment,replay_name) {
     params={
        parent_id:parent_id,
        content:comment,
        new_id:GetRequest().new_id
    };
    $.ajax({
        url:host+"/news/comment/",
        type: "post",
        headers:{
            "Authorization": "JWT " + token
        },
        data : params,

        ContentType:"application/json"
    }).done(function (resp) {
         content = "<div class='reply_list'>  <div data_id='"+resp.id+"'>";
        content +="<a class='ft_blue can_reply' data_id='"+resp.id+"' title='点击回复他' href='javascript:;'>"+resp.user.username+ "</a> 回复"+replay_name+resp.content;
        content += "<a href='javascript:;' data_id='"+resp.id+"' class='comment_report' data-type='reply'>举报</a>";
        content += "<a href='javascript:;' class='float-right comment_like '>"+resp.like+" 赞</a>  </div>  </div>";

        //孙子评论显示与父评论同级
        $("div[data_id="+parent_id+"]").parent().after(content);
        //文本输入框隐藏
            $(".reply_input").remove();
            reply_input_flag = 0;
    })
}

//递归显示子评论
function generate(data,replay_name) {
    if(!data){
        return;
    }
    for(var m=0;m<data.length;m++){
        con = data[m];
        content = "<div class='reply_list'>  <div data_id='"+con.id+"'>";
        content +="<a class='ft_blue can_reply' data_id='"+con.id+"' title='点击回复他' href='javascript:;'>"+con.user.username+ "</a> 回复"+replay_name+" :  "+con.content;
        content += "<a href='javascript:;' data_id='"+con.id+"' class='comment_report' data-type='reply'>举报</a>";
        content += "<a href='javascript:;' class='float-right comment_like '>"+con.like+" 赞</a>  </div>  </div>";

        //添加到全局数组中
        comment_list.push(content);
        if(con.subs){
           generate(con.subs,con.user.username);

    }
        }

}

//存放显示评论的数据
var comment_list = [];

//显示该新闻的评论信息
function Show_New_Comment() {
    var data ={
        "ordering":"-report_time",
        "page":cur_page,
        "page_size":page_size
    };
    $.ajax({
        url:host+"/news/comment/?new_id="+GetRequest().new_id,
        type: "get",
        ContentType:"application/json",
        data:data
    }).done(function (resp) {
        total_page = resp.total_page;

        //判断评论是否已经到底了
        if(cur_page<total_page){
        $(".is_bottom").hide();
        $(".comment_tip").show();
    }else{
          $(".is_bottom").show();
        $(".comment_tip").hide();
        }


         for(i=0;i<resp.data.length;i++){
                var contents = resp.data[i];
              content = "<li data_id='"+contents.id+"'>";
                if(contents.user.avatar_url){
                    content +="<img src='"+contents.user.avatar_url+"'>";
                }else{
                    content +="<img src='img/person.jpeg'>";
                }
                content +="<div class='comment-box'> <span class='comment_nickname' user_id='"+contents.user.id+"'>"+contents.user.username+"</span>";
                    content +="<span class='comment_date'>"+contents.create_time+"</span>";
                            content += "<a class='comment_report' href='javascript:;' data_id='"+contents.id+"' data-type='comment'>举报";
                            content += "</a><a href='javascript:;' class='comment_reply' replay_id='"+contents.id+"'>回复</a>";
                            content += "<a href='javascript:;' class='float-right comment_like '>"+contents.like +"赞</a> </div> <p>"+contents.content+"</p>";

             comment_list.push(content);
                            //判断是否有子评论
                            if(contents.subs){
                            //遍历子评论
                            for(var a =0;a<contents.subs.length;a++){
                                var kk = contents.subs;
        var con = kk[a];
        content = "<div class='reply_list'>  <div data_id='"+con.id+"'>";
        content +="<a class='ft_blue can_reply' title='点击回复他' href='javascript:;'>"+con.user.username+": </a>"+con.content;
        content += "<a href='javascript:;' data_id='"+con.id+"' class='comment_report' data-type='reply'>举报</a>";
        content += "<a href='javascript:;' class='float-right comment_like '>"+con.like+" 赞</a>  </div>  </div>";
                //通过数组添加
                comment_list.push(content);
                //递归子子评论
                   if(con.subs){

                       generate(con.subs,con.user.username);
                   }
                            }
                             }


                            comment_list.push("</li>");
                            //往页面中添加数据
             $($.parseHTML(comment_list.join(" "), document, true)).appendTo(".comment_list");
             // $(".comment_list").append();
             comment_list = [];

         }



    })
}


$(function () {

    //判断评论是否已经到底了
    $(".comment_tip").click(function () {
        cur_page += 1;
        //获取评论信息
        Show_New_Comment();
    });



    //获取新闻内容
    GetDetailNew();

    //获取关注状况
    GetFollow();

    //关注的鼠标移入移除样式
    FocusStyle();

    //获取评论信息
    Show_New_Comment();

    //点击关注按钮事件
    $(".focus").click(function () {
        //判断用户是否登录
        if(judge_user()){
        //    发送请求该用户关注该作者
        Followed();
    }else {
    //   将关注显示

        $(".login_form_main").show();
        $(".mask").show();
        mask_flag=2;
    }
    });

    //取消关注按钮点击
    $(".unfocus").click(function () {
        //取消关注
        Remove_Follow();
    });

    //添加父评论\子评论
    $(document).on("click ",".add-comment-btn",function(){
        //判断用户是否登录
        if(judge_user()){
            //有两个btn如果能找到data_id的话就是parent_id
            parent = $(this).parent().siblings(".reply_textarea").attr("data_id");

            if(parent){
                comment = $(this).parent().siblings(".reply_textarea").val();
                parent_id = parent;
                Add_comment(parent_id,comment);

            }else {
                parent_id = "null";
                Add_comment(parent_id,$(".comment_input").val());
            }
        //    发送评论请求
    }else {
    //   将关注显示

        $(".login_form_main").show();
        $(".mask").show();
        mask_flag=2;
    }});

    //添加子评论点击发送添加评论
     $(document).on("click ",".add-reply-btn",function(e){
        //判断用户是否登录
        if(judge_user()){
            //父id
            par = $(this).parent().siblings(".subs_reply_textarea").attr("data_id");
            //评论内容
            con = $(this).parent().siblings(".subs_reply_textarea").val();
            //回复评论名字
            reply_name =$(this).parent().siblings(".subs_reply_textarea").attr("placeholder");
        //    发送评论请求
        subs_Addcomment(par,con,reply_name);

    }else {
    //   显示需要登录
        $(".login_form_main").show();
        $(".mask").show();
        mask_flag=2;
    }
         });

    //回复按钮事件
     var reply_input_flag = 0;
    $(document).on("click ",".comment_reply",function(e){
        if(reply_input_flag==1){
            $(".reply_input").remove();
            reply_input_flag = 0;
            return;
        }
         e.stopPropagation();
        content=" <div class='reply_input'> <textarea class='reply_textarea' placeholder='回复"+$(this).siblings(".comment_nickname").html()+":' data_id='"+$(this).parents("li")[0].attributes[0].value +"'>";
        content += "</textarea> <p><span class='add-comment-btn'>发表</span></p> </div>";

        // $(this).parents("li").append(content);
        $(this).parent().next().after(content);
        reply_input_flag = 1;

});

    //子评论按钮时间
     var subs_reply_input_flag = 0;
    $(document).on("click ",".can_reply",function(e){

        if(subs_reply_input_flag==1){
            $(".reply_input").remove();
            subs_reply_input_flag = 0;
            return;
        }

         e.stopPropagation();
        content=" <div class='reply_input'> <textarea class='subs_reply_textarea' placeholder='"+$(this).html()+"' data_id='"+$(this).parent().attr("data_id") +"'>";
        content += "</textarea> <p><span class='add-reply-btn'>发表</span></p> </div>";

        $(this).parent().after(content);
        subs_reply_input_flag = 1;
});


    //点击时取消回复
    // $("body").click(function () {
    //     $(".reply_input").remove();
    // })

});