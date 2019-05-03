from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    #获取新闻列表
    url(r'^list/(?P<pk>\d+)/category$', views.Get_Newslist_ListApiView.as_view()),

    #广告轮播图
    url(r'^slideshow/$', views.Get_Slideshow_Apiview.as_view()),

    #精选新闻
    url(r'^good/$', views.GetGoodNews.as_view()),

    #主页面
    url(r'^category/$', views.Category_info.as_view()),

    #获取搜索关键字
    url(r'^keysword/$', views.Get_Search_Keyswords.as_view()),

    #添加评论信息
    url(r'^comment/$', views.New_Comment.as_view()),

    #获取作者新闻列表
    url(r'^author/(?P<pk>\d+)/list/$', views.Author_Newlist.as_view()),

    #获取新闻搜索
    url(r'^search/$', views.NewsSearchView.as_view()),

    # 作者中心新闻图片上传
    url(r'^image_upload/$', views.NewsImageUpload.as_view()),

    #作者新闻上传
    url(r'^upload/$',views.NewContent_upload.as_view()),

    #获取作者新闻上传状态
    url(r'^author/status_info/$',views.Author_News_Status.as_view()),

    #作者上传后新闻的修改
    url(r'^author/(?P<pk>\d+)/update/$',views.Author_News_Update.as_view()),







]

router = DefaultRouter()

#获取新闻详情页数据
router.register('detail',views.New_Detail_ViewSet,base_name='newsdeatil_manager')

urlpatterns +=router.urls

print(urlpatterns)