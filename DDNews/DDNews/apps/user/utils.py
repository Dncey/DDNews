from django.contrib.auth.backends import ModelBackend
import  re

from news.models import User

#默认jwt返回格式
# def jwt_response_payload_handler(token, user=None, request=None):
#     return {
#         'token': token,
#         'username': user.username,
#         'user_id':user.id,
#         'avatar_url':user.avatar_url,
#     }



class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if re.match(r'1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except:
            user = None
        if user and user.check_password(password):
            return user
