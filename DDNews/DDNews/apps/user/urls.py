from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.IndexView),

    # 查询该用户是否关注该作者
    url(r'^author/(?P<pk>\d+)/followed/$', views.GetUserfollowd.as_view()),
]

print(urlpatterns)