var currentCid = 0; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据
var page_size = 8;

$(function () {

    //获取分类信息
    getCategoryinfo();

    //更新新闻列表
    updateNewsData();
    //获取首页广告轮播图
    updateNewsSlideshow();

    //获取精选新闻
    GetGoodNews();

    //获取推荐作者
    GetGoodAuthor();


    //  解决dom生成html无法触发js事件
    $(document).on("click",".item",function(){//修改成这样的写法
    var clickCid = $(this).attr("category_id");
        // $(".list .item").each(function () {
        //     $(this).removeClass("active")
        // })
        // $(this).addClass("active")


        $(this).addClass("item_style").siblings().removeClass("item_style");

        if(clickCid ==0){
            $(".slide_show").css({"display":"block"});
            $(".articles").css({"margin-top":"350px"});
        }else {
            $(".slide_show").css({"display":"none"});
            $(".articles").css({"margin-top":"-20px"});
        }


        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid;

            // 重置分页参数
            cur_page = 1;
            total_page = 1;
            updateNewsData();
        }
});
    // 首页分类切换
    $(".item").click(function () {
        var clickCid = $(this).attr("category_id");
        // $(".list .item").each(function () {
        //     $(this).removeClass("active")
        // })
        //添加效果


        if(clickCid ==0){
            $(".slide_show").css({"display":"block"});
            $(".articles").css({"margin-top":"350px"});
        }else {
            $(".slide_show").css({"display":"none"});
            $(".articles").css({"margin-top":"-20px"});
        }


        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid;

            // 重置分页参数
            cur_page = 1;
            total_page = 1;
            updateNewsData();
        }
    });

    //页面滚动加载相关
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
            if(!data_querying){
                data_querying = true;
                if(cur_page<total_page){
                    cur_page +=1;
                    updateNewsData();
                }else {
                    content = "<div class='errorinfo'>新闻已经到底了，请稍后刷新</div>";
                $(".articles").append(content);
                }

            }
        }
    });


    //跳转作者中心页面
    $(document).on("click",".author",function(event){
        //阻止父类点击对自己的影响，阻止事件冒泡
        event.stopPropagation();
        var user_id = $(this).attr("author_id");
        location.href ="author_center.html?author_id="+user_id;
    });

    //跳转新闻详情页
    $(document).on("click",".article",function(){
        var new_id = $(this).attr("new_id");
        location.href ="detail.html?new_id="+new_id;
    });










});


//获取精选新闻
function GetGoodNews() {
    $.ajax({
        url:host+"/news/good/",
        type: "GET",
        ContentType:"application/json"
    }).done(function (resp) {

        for(var i=0;i<resp.length;i++){
            good_new = resp[i];

            content ="<div class='new_list'><a class='doc' title='"+good_new.title+"' href='detail.html?new_id="+good_new.id+"'> <div class='doc_icon '>";
            if(i==0){
                content +="<span class='first_icon'>1 </span>"
            }else if(i==1){
                content +="<span class='second_icon'>2 </span>"
            }else if(i==2){
                content +="<span class='third_icon'>3 </span>"
            }else {
                content +="<span class='doc_icon'>"+(i+1)+"</span>"
            }

            content +="</div> <div class='doc_title'>"+good_new.title+" </div> </a> </div>";
            $(".select_news").append(content)
        }

    })

}

//获取推荐作者

function GetGoodAuthor() {
     $.ajax({
        url:host+"/user/good/",
        type: "GET",
        ContentType:"application/json"
    }).done(function (resp) {
        for(var b=0;b<resp.length;b++){
            author =resp[b];

            content = "<a class='doc' href='author_center.html?author_id="+author.id+"'><div class='doc_image_small_wrapper'>";

            content += "<img class='doc_image_small' src='"+author.avatar_url+"'> </div> <div class='doc_content'>  <div class='doc_content_inline'>";
            content +=" <div class='author_title'>"+author.username+"</div>";
            content +=" <div class='doc_info'> <div class='summary'>"+author.signature+"</div> </div> </div> </div> </a>";

            $(".right_top > .content").append(content);

        }

     });
}


//更新主页轮播图
function updateNewsSlideshow() {
    //获取首页广告轮播图
    $.ajax({
        url:host+"/news/slideshow/",
        type: "GET",
        ContentType:"application/json"
    }).done(function (resp) {
        $(".slide_show").html("");
        for(var i=0;i<resp.data.length;i++){
            var news = resp.data[i];
            if (i!=0){
               var style = "style='display: none;'";
               content = " <a class='slide_item' href='detail.html?new_id="+news.new_id+"' target='_blank'"+style+">";
            }else {
                style = "style='display: inline;'";
              content = "<a class='slide_item' href='detail.html?new_id="+news.new_id+"' target='_blank'"+style+">";
            }

            content += " <img src='"+news.image_url+"'>";
            content +=" <div class='slide_shadow'>  </div> <p class='slide_item_title'>"+news.title +"</p> </a>";
            $(".slide_show").append(content);
        }
        content = "<div class='wrapper_radios'> <div class='item_radios active'></div> <div class='item_radios'></div> <div class='item_radios'></div>"
        $(".slide_show").append(content);
    }).fail(function () {

    })
}

//更新新闻列表数据
function updateNewsData() {
    // TODO 更新新闻数据
    var data ={
        "ordering":"-report_time",
        "page":cur_page,
        "page_size":page_size
    };
    $.ajax({
        url: host+"/news/list/"+currentCid+"/category",
        type: "GET",
        ContentType:"application/json",
        data:data
    })
    .done(function(resp) {
     total_page = resp.total_page;
            if(cur_page==1){
                $(".articles").html("");
            }
            for(var i=0;i<resp.data.length;i++){
                var news = resp.data[i];
                var source_avatar_url = "";
                //判断该新闻是否是爬取的，如果是则判断是否有索引头像，如果不是则是用户自己上传的，查看用户的索引头像
                if (news.is_spider){
                    if(news.source_avatar_url){
                        source_avatar_url = news.source_avatar_url;
                    }else {
                        source_avatar_url = "/static/news/img/person.jpeg";
                    }
                }else {
                    if(news.user.avatar_url){
                        source_avatar_url = news.user.avatar_url;
                    }else {
                        source_avatar_url = "/static/news/img/person.jpeg";
                    }
                }

            // 把拼接后的新闻数据，重新添加到ul列表下
                if(news.index_image_url ==null ||news.index_image_url ==""){
                    content = "<li class='article' new_id='"+news.id+"'> <a  class='news_title'>"+news.title+"</a>";
                    content +="<a class='news_detail_none'>"+news.title+"</a>";
                    content +="<div class='author_info' > <div class='author' author_id='"+news.user.id+"'><a  class='person_icon'><img src='";
                     content +=source_avatar_url+"'></a> <a";
                     content +=" class='author_name'>"+news.source+"</a> </div> <div class='time'>";
                    content +=news.report_time+"</div> </div> </li>"
                }else {
                    content  = "<li class='article' new_id='"+news.id+"'> " ;
                    content +=" <a class='article_prc'><img src='"+news.index_image_url;
                    content +="'></a> <a class='news_title'>" +news.title;
                    content +="</a> <a  class='news_detail'>"+news.digest;
                    content +="</a> <div class='author_info'> <div class='author' author_id='"+news.user.id+"' ><a  class='person_icon'><img src='";
                    content +=source_avatar_url+"'></a> <a";
                     content +=" class='author_name'>"+news.source+"</a> </div> <div class='time'>";
                    content +=news.report_time+"</div> </div> </li>"
                }

                $(".articles").append(content);
                data_querying = false;
                }
    })
    .fail(function() {
        // alert("服务器超时，请重试！");
    });
}





