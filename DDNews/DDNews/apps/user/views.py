from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from news.models import User_Fans,News,User
from rest_framework.response import Response
import rest_framework_jwt.authentication


#查询是否关注
class GetUserfollowd(APIView):
    def get(self,request,pk):
        new_id =pk
        try:
            new = News.objects.get(id=new_id)
        except:
            return Response({'errmsg':'查询新闻失败'})
        author_id = new.user_id

        user = request.user
        user_id = user.id
        try:
            user_fan = User_Fans.objects.filter(follow_id=author_id,fan_id=user_id)
        except:
            return Response({'errmsg':'查询数据失败'})

        if not user_fan:
            return Response({'data':'false'})
        return Response({'data':'true'})

#关注与取消关注
class User_Followed(APIView):
    def post(self,request):
        author_id = request.data.get('author_id')
        user = self.request.user

        if user.id == int(author_id):
            return Response({"errmsg":"自己不能关注自己"})

        try:
            author = User.objects.get(id=author_id)
        except:
            return Response({'errmsg':'获取作者信息失败'})

        if not author:
            return Response({'errmsg':'作者不存在'})


        User_Fans.objects.create(fan=user,follow=author)


        return Response({'errmsg':'OK'})


    def delete(self,request):
        author_id = request.data.get('author_id')
        user = self.request.user

        try:
            author = User.objects.get(id=author_id)
        except:
            return Response({'errmsg':'获取作者信息失败'})

        if not author:
            return Response({'errmsg':'作者不存在'})


        user_fans = User_Fans.objects.filter(fan=user, follow=author).first()
        if not user_fans:
            return Response({'errmsg':'参数错误'})

        user_fans.delete()
        return Response({'errmsg':'OK'})