var currentCid = 0; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var page_size = 9;


//查询是否关注
function GetFollow_Author() {
     $.ajax({
        url: host + "/user/" + GetRequest().author_id + "/follow/",
        type: "get",
        headers:{
            "Authorization": "JWT " + token
        },
        ContentType:"application/json"
    }).done(function (resp) {
        if(resp.data == "true"){
            $(".unfocus").css({"display": "inline-block"});
            $(".focus").css({"display": "none"});
        }else{
            $(".unfocus").css({"display": "none"});
        $(".focus").css({"display": "inline-block"});
        }
    }).fail(function (resp) {
        console.log("获取信息失败");

    });
}

//关注该作者
//发起关注请求
function Followedd() {
    params = {
        author_id: GetRequest().author_id,
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
    });
}

//获取作者信息+精选新闻
function Get_Author_info() {
   $.ajax({
        url: host + "/user/author/"+GetRequest().author_id+"/info/",
        type: "get",
        ContentType:"application/json"
    }).done(function (resp) {
        //添加作者名字
        $(".author_nickname").html(resp.username);
        //判断作者是否有头像
        if(resp.avatar_url){
         $(".author_avatar").attr("src",resp.avatar_url);
        }
        //添加作者id方便后续发送
        $(".author_head").attr("author_id",resp.id);
        //作者关注
       followed = "<h3 riot-tag='number' number='"+resp.followed+"'><em class='y-number'><i>"+resp.followed+"</i></em></h3>";

       $("dt a[ga_event='nav_user_list']").prepend(followed);

       fans = "<h3 riot-tag='number' number='"+resp.fans+"'><em class='y-number'><i>"+resp.fans+"</i></em></h3>";
       $("dd a[ga_event='nav_user_list']").prepend(fans);


       //近期佳文
       for(var i=0;i<resp.good_articles.length;i++){
           new_list = resp.good_articles[i];
           if(i%2==0){
               //样式一
               content = "<li> <div class='line'>  <div class='rbox'> <div class='rbox-inner'> <a target='_blank' title='"+new_list.title+"' href='detail.html?new_id="+new_list.id+"'>"+new_list.title+"</a> <span>"+new_list.clicks+"阅读</span>  </div> </div> </div> </li>"
           }else{
               //样式二
               content = "<li> <div class='line image'> <a class='lbox' target='_blank' href='detail.html?new_id="+new_list.id+"'> <img alt='' src='//"+new_list.index_image_url+"'>   </a> <div class='rbox'> <div class='rbox-inner'> <a target='_blank' title='"+new_list.title+"detail.html?new_id="+new_list.id+"'>"+new_list.title+"</a> <span>"+new_list.clicks+"阅读</span>  </div> </div> </div> </li>"
           }
           $(".recent ul").append(content);


       }

    })
}

//取消关注
function Remove_Follows() {
    params = {
        author_id: GetRequest().author_id
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

//作者新闻列表
function updateAuthorNewsData() {
    // TODO 更新作者新闻数据
    var data ={
        "ordering":"-report_time",
        "page":cur_page,
        "page_size":page_size
    };
    $.ajax({
        url: host+"/news/author/"+GetRequest().author_id+"/list/",
        type: "GET",
        ContentType:"application/json",
        data:data
    })
    .done(function(resp) {
     total_page = resp.total_page;
            if(cur_page==1){
                $(".articles").html("");
            }

            for(var i=0;i<resp.data.length;i++) {
                var news = resp.data[i];
                if(news.index_image_url !=null){
                content = "<li class='article'> <a href='detail.html?new_id=" + news.id + "' class='article_prc'><img src='//" + news.index_image_url + "' style='display: inline-block; width: 150px; height: 100px;'></a>";content += " <div class='rbox-inner'> <div class='title-box'> <a class='title-box' href='detail.html?new_id=" + news.id + "' target='_blank'>" + news.title + "</a>";
                content += "</div>  <div class='y-box footer'> <div class='y-left'>  <a class='lbtn' target='_blank' href='detail.html?new_id=" + news.id + ">" + news.clicks + "阅读&nbsp;⋅</a>  <a class='lbtn' href='javascript:;' target='_blank'>&nbsp;" + news.comment + "评论&nbsp;</a> <div class='time'>" + news.report_time + "</div>     </div>  </div> </div>   </li>";
            }else{
                    content = "<li class='article'>  <div class='rbox-inner'> <div class='title-box'> <a class='title-box' href='detail.html?new_id=" + news.id + "' target='_blank'>" + news.title + "</a>";
                content += "</div>  <div class='y-box footer'> <div class='y-left'>  <a class='lbtn' target='_blank' href='detail.html?new_id=" + news.id + ">" + news.clicks + "阅读&nbsp;⋅</a>  <a class='lbtn' href='javascript:;' target='_blank'>&nbsp;" + news.comment + "评论&nbsp;</a> <div class='time'>" + news.report_time + "</div>     </div>  </div> </div>   </li>";
                }

                $(".articles").append(content);
                }
    });

}

//获取当前作者关注的用户
function GetFollowed() {
    $.ajax({
        url: host + "/user/author/"+GetRequest().author_id+"/followed/",
        type: "get",
        ContentType:"application/json"
    }).done(function (resp) {
        alert("ddd");
    })

}

//获取当前作者的粉丝
function GetAuthor_Fans() {
     $.ajax({
        url: host + "/user/author/"+GetRequest().author_id+"/fans/",
        type: "get",
        ContentType:"application/json"
    }).done(function (resp) {

    })
}


$(function () {

//关注鼠标移入移除效果
    FocusStyle();

//获取关注状况
    new GetFollow_Author();

    //获取作者信息
    Get_Author_info();


    //点击关注按钮事件
    $(".focus").click(function () {
        //判断用户是否登录
        if(judge_user()){
        //    发送请求该用户关注作者
        Followedd();
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
        Remove_Follows();
    });

    //获取新闻
    updateAuthorNewsData();

     //页面滚动加载,刷新新闻
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 2) {
            // TODO 判断页数，去更新新闻数据
            if(currentCid==0){
                if(cur_page<total_page){
                    cur_page +=1;
                    updateAuthorNewsData();
                }else {
                    content = "<div class='errorinfo'>新闻已经到底了</div>";
                $(".articles").append(content);
                }

            }
        }
    });


    //当前作者的新闻
    $("li[code='a']").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
        currentCid =0;
        $(".article").html("");
        updateAuthorNewsData();
    });

    //查看我的关注
    $("li[code='d']").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
        currentCid = 1;
        $(".articles").html("");
        GetFollowed();

    });
    //查看我的粉丝
    $("li[code='b']").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
        currentCid =2;
        $(".articles").html("");
        GetAuthor_Fans()
    })

});