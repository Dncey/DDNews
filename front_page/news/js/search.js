/**
 * Created by python on 19-4-25.
 */

var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var page_size = 9;
var click_id =1;
var current_id=1;

// 搜索新闻
function updateSearchNewsData() {
    var data ={
        "ordering":"-report_time",
        "page":cur_page,
        "page_size":page_size,
        "keywords":GetRequest().search_keywords
    };
    $.ajax({
        url:host+"/news/search/",
        type: "get",
        ContentType:"application/json",
        data:data
    }).done(function (resp) {
        total_page = resp.total_page;
           if(cur_page==1){
                $(".articles").html("");
            }
            for(var i=0;i<resp.data.length;i++) {
                var news = resp.data[i];
                if(news.index_image_url !=null){
                content = "<li class='article'> <a href='detail.html?new_id=" + news.id + "' class='article_prc'><img src='" + news.index_image_url + "' style='display: inline-block; width: 150px; height: 100px;'></a>";content += " <div class='rbox-inner'> <div class='title-box'> <a class='title-box' href='detail.html?new_id=" + news.id + "' target='_blank'>" + news.title + "</a>";
                content += "</div>  <div class='y-box footer'> <div class='y-left'>  <a class='lbtn' target='_blank' href='detail.html?new_id=" + news.id + ">" + news.clicks + "阅读&nbsp;⋅</a>  <a class='lbtn' href='javascript:;' target='_blank'>&nbsp;" + news.comment + "评论&nbsp;</a> <div class='time'>" + news.report_time + "</div>     </div>  </div> </div>   </li>";
            }else{
                    content = "<li class='article'>  <div class='rbox-inner'> <div class='title-box'> <a class='title-box' href='detail.html?new_id=" + news.id + "' target='_blank'>" + news.title + "</a>";
                content += "</div>  <div class='y-box footer'> <div class='y-left'>  <a class='lbtn' target='_blank' href='detail.html?new_id=" + news.id + ">" + news.clicks + "阅读&nbsp;⋅</a>  <a class='lbtn' href='javascript:;' target='_blank'>&nbsp;" + news.comment + "评论&nbsp;</a> <div class='time'>" + news.report_time + "</div>     </div>  </div> </div>   </li>";
                }

                $(".articles").append(content);
                }
    }).fail(function (resp) {
        if(resp.status==400){
            alert(resp.responseJSON.errmsg)
        }
    });

}

// 搜索用户
function updateSearchUser() {
    $.ajax({
        url: host + "/user/search/?user="+GetRequest().search_keywords,
        type: "get",
        ContentType:"application/json"
    }).done(function (resp) {
        total_page = resp.total_page;
           if(cur_page==1){
                $(".articles").html("");
            }
        for(var i=0;i<resp.length;i++){
            con = resp[i];
        content = "<li class='author_card card_list'> <a href='author_center.html?author_id="+con.id+"' target='_blank' class='author_pic'><img src='"+con.avatar_url+"'></a>";

        content += "<a href='author_center.html?author_id=" +con.id+"' target='_blank' class='author_name'>"+con.username+"</a>";
        content += "<div class='author_resume'>"+con.signature+"</div>";
        content += "<a href='javascript:;'class='focus float'> <i>+</i> 关注 </a> <a href='javascript:;'  class='unfocus float'>   <i>-</i> <span class='out'> 已关注 </span> <span class='over'> 取消关注</span> </a></li>";
        $(".articles").append(content);
        }
    }).fail(function (resp) {
        if(resp.status==400){
            alert(resp.responseJSON.errmsg)
        }
    });
}


//获取分类信息
function getSearchCategoryinfo() {
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
                    $(".list").append(content1);
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

$(function () {

    //获取新闻分类
    getSearchCategoryinfo();

    updateSearchNewsData();

    //搜索文章
    $(".article_search").click(function () {

        cur_page=1;
        current_id =1;
        $(".articles").html("");
        updateSearchNewsData();


    });
    // 搜索用户
    $(".user").click(function () {
        cur_page=1;
        current_id=2;
        $(".articles").html("");

        updateSearchUser();
        cur_page +=1;

    });

    $(".xbox >li").click(function () {
        $(this).addClass("item_border").siblings().removeClass("item_border")
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
            if(current_id==1){

                if(cur_page<total_page){
                    cur_page +=1;
                    updateSearchNewsData();
                }else {
                    content = "<div class='errorinfo'>新闻已经到底了，请稍后刷新</div>";
                $(".articles").append(content);
                }

            }else {
                if(cur_page<total_page){
                    cur_page +=1;
                     updateSearchUser();
                }else {
                    content = "<div class='errorinfo'>用户信息已经到底了，请稍后刷新</div>";
                $(".articles").append(content);
                }
            }
        }
    });
});