from django.conf.urls import url
from . import views

urlpatterns = [
    #图片验证码
    url(r'^img_code/(?P<uuid>\w+-\w+-\w+-\w+-\w+)/$', views.Generate_ImageCode.as_view()),
    #获取手机验证码
    url(r'^sendSMSCode/register/$',views.Generate_Smscode_register.as_view()),
    #发送找回密码的验证码
    url(r'^sendSMSCode/forget/$',views.Generate_Smscode_forget.as_view()),
    #用户注册
    url(r'^register/$',views.User_Register.as_view()),
    #用户登录
    url(r'^login/$',views.User_Login.as_view()),

    #用户忘记密码
    url(r'^resetpwd/$',views.User_ResetPwd.as_view()),
]

print(urlpatterns)