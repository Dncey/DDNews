from django.conf.urls import url
from . import views

urlpatterns = [
    #获取新闻列表
    url(r'^list/(?P<pk>\d+)/category$', views.Get_Newslist_ListApiView.as_view()),

    #广告轮播图
    url(r'^slideshow/$', views.Get_Slideshow_Apiview.as_view()),

    #主页面
    url(r'^category/$', views.Category_info.as_view()),

    #获取搜索关键字
    url(r'^keysword/$', views.Get_Search_Keyswords.as_view()),

]

print(urlpatterns)