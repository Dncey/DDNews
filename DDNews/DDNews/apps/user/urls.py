from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.IndexView),

    # 查询该用户是否关注new_id作者
    url(r'^author/(?P<pk>\d+)/follow/$', views.GetUserfollowd.as_view()),
    # 查询是否关注个作者
    url(r'^(?P<pk>\d+)/follow/$', views.GetUserfollow.as_view()),

    #查询推荐作者
    url(r'^good/$', views.GetGoodAuthor.as_view()),

    #关注该用户
    url(r'^author/followed/$', views.User_Followed.as_view()),
    #获取该作者的信息
    url(r'^author/(?P<pk>\d+)/info/$', views.GetAuthor_Info.as_view()),

    #获取作者的粉丝
    url(r'^author/(?P<pk>\d+)/fans/$', views.GetAuthor_Fans.as_view()),

    #获取作者的关注
    url(r'^author/(?P<pk>\d+)/followed/$', views.GetAuthor_Followed.as_view()),

    #获取用户相关搜索
    url(r'^search/$',views.UserSearchView.as_view()),

    #用户中心获取\修改用户详情信息
    url(r'(?P<pk>\d+)/info/$',views.GetUserBaseInfo.as_view()),


    url(r'(?P<pk>\d+)/password/$',views.Change_User_Password.as_view()),

]

print(urlpatterns)