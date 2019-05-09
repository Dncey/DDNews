from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from news.models import User
import hashlib


class Admin_Login(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        md5 = hashlib.md5()
        md5.update(password.encode())
        # 获取MD5加密后的值
        passwd = md5.hexdigest()


        user = User.objects.filter(username=username,password=passwd,is_superuser=1).first()

        if not user:
            return Response({'errmsg':'用户名或密码错误'},status=400)


        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data = {
            'token':token,
            'user_id':user.id,
            'username':user.username,
            'avatar_url':user.avatar_url,
            'is_admin':'true'
        }

        return Response(data)