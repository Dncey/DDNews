"""DDNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from rest_framework_jwt.views import verify_jwt_token
from django.contrib import admin
import news

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^/', news.views.IndexView),
    #新闻模块
    url(r'^news/', include('news.urls')),
    #登录注册相关模块
    url(r'^passport/', include('passport.urls')),
    #用户模块
    url(r'^user/', include('user.urls')),
    #管理员
    url(r'^admin/', include('pandaNewAdmin.urls')),
    #验证jwt
    url(r'^judge_jwt/$', verify_jwt_token),
]
