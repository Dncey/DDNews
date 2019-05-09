from django.conf.urls import url
from . import views


urlpatterns = [

    #管理员登录
    url(r'^login/$',views.Admin_Login.as_view()),
]