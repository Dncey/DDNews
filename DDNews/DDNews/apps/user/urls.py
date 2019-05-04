from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.IndexView),


    #用户收藏的添加和取消
    url(r'^news/collected/$', views.UserNewCollection.as_view()),

    # 查询该用户是否关注new_id作者 新闻详情页
    url(r'^author/(?P<pk>\d+)/follow/$', views.GetUserFollowAndCollection.as_view()),

    # 查询是否关注该作者　　作者中心页
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

    #用户密码修改
    url(r'(?P<pk>\d+)/password/$',views.Change_User_Password.as_view()),

    #用户头像上传
    url(r'(?P<pk>\d+)/avatar/$',views.UploadUserAvatar.as_view()),

    #作者中心获取收藏新闻信息
    url(r'news/collection/$',views.GetUserNewsCollections.as_view()),

]

print(urlpatterns)