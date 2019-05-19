from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [

    #管理员登录
    url(r'^login/$',views.Admin_Login.as_view()),

    #用户月每日活跃度统计
    url(r'^user_day_active/$',views.User_Day_Active.as_view()),

    #新闻数据分析
    url(r'^news_analysis/$',views.News_Detail_Analysis.as_view()),

    #管理员审核页面
    url(r'^author/news/$',views.AllAuthor_Newlist.as_view()),

    #新闻审核
    url(r'^author/new/(?P<pk>\d+)/review/$',views.Author_New_Review.as_view()),

    # 广告轮播图信息的获取
    url(r'^slide_new/$', views.Get_New_Slide.as_view()),

    #广告轮播添加和修改和删除
    url(r'^(?P<pk>\d+)/slide_new/$',views.New_Slide.as_view()),

]

