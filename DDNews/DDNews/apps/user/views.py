from django.db.models import Count
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView,ListAPIView,GenericAPIView
from news.models import User_Fans,News,User
from rest_framework.response import Response
import rest_framework_jwt.authentication
from .serializers import GetAuthor_Info_Serializer,Author_Fans, Author_Followed,User_Avatar_Url_Serializer
import hashlib



# 首页获取推荐用户
class GetGoodAuthor(APIView):
    def get(self,request):

        user_list = []
        #通过新闻表查询用户发布的新闻量前三的用户ｉｄ,且新闻状态为审核通过
        users =News.objects.values('user_id').filter(status=0).exclude(user_id=1).annotate(all_id=Count('id'))[:3]
        #强转换成列表
        users = list(users)
        #排序,从大到小排序
        users = sorted(users,key=lambda users:users['all_id'],reverse=True)

        print(users)
        for user_id in users:
            dict={}
            user = User.objects.get(id=user_id['user_id'])
            dict['id']=user.id
            dict['username']=user.username
            dict['signature']=user.signature
            dict['avatar_url']=user.avatar_url
            user_list.append(dict)

        return Response(user_list)




#查询是new_id否关注
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


#author_id是否关注
class GetUserfollow(APIView):
    def get(self,request,pk):

        author_id = pk
        user = request.user
        user_id = user.id
        try:
            user_fan = User_Fans.objects.filter(follow_id=author_id,fan_id=user_id)
        except:
            return Response({'errmsg':'查询数据失败'})

        if not user_fan:
            return Response({'data':'false'})
        return Response({'data':'true'})

#获取作者信息
class GetAuthor_Info(RetrieveAPIView):
    serializer_class = GetAuthor_Info_Serializer
    def get_object(self):
        pk = self.kwargs['pk']
        try:
            User.objects.get(id=pk)
        except:
            return Response({'errmsg':'参数错误'})

        return User.objects.get(id=pk)

#获取作者的粉丝
class GetAuthor_Fans(ListAPIView):
    serializer_class = Author_Fans
    def get_queryset(self):
        pk = self.kwargs['pk']
        return User_Fans.objects.filter(follow_id=pk)

#获取作者的关注
class GetAuthor_Followed(ListAPIView):
    serializer_class = Author_Followed
    def get_queryset(self):
        pk = self.kwargs['pk']
        return User_Fans.objects.filter(fan_id=pk)

#搜索用户表
class UserSearchView(ListAPIView):
    serializer_class = User_Avatar_Url_Serializer
    def get_queryset(self):
        pk = self.request.query_params.get("user")
        user= User.objects.filter(username__contains=pk)
        return user

    # 去掉self.request可以让图片没有本地域名的前缀
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }


#获取\修改用户信息
class GetUserBaseInfo(APIView):
    def get(self,request,pk):
        user_id = pk

        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"errmsg":"用户数据错误"},status=400)

        user_info ={}

        user_info['avatar_url']=user.avatar_url
        user_info['signature'] = user.signature
        user_info['username'] = user.username
        user_info['gender'] = user.gender

        # 返回数据
        return Response({'data':user_info})



    def put(self,request,pk):
        user_id = pk
        nick_name = request.data.get("nick_name")
        signature = request.data.get("signature")
        gender = request.data.get("gender")

        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"errmsg":"用户数据错误"})
        if(len(signature)>50 | len(nick_name)>25):
            return Response({'errmsg':'用户名或签名过长'},status=400)

        #判断性别是男是女
        if gender =="man":
            user.gender = 1
        elif gender =="women":
            user.gender = 2
        else:
            return Response({'errmsg':'错误参数'},status=400)

        user.signature =signature
        user.username = nick_name
        try:
            user.save()
        except Exception as e:
            return Response({'errmsg':'保存失败'})

        #返回数据
        user_info = {}

        user_info['avatar_url'] = user.avatar_url
        user_info['signature'] = user.signature
        user_info['username'] = user.username
        user_info['gender'] = user.gender

        return Response({'data': user_info})


#修改用户密码
class Change_User_Password(APIView):
    def put(self,request,pk):
        user_id = pk
        local_password = request.data.get("local_password")
        change_password= request.data.get("change_password")
        confirm_password = request.data.get("confirm_password")

        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"errmsg": "用户数据错误"}, status=400)

        #判断是否为空
        if not all([local_password,change_password,confirm_password]):

            return Response({"errmsg": "密码有空值"}, status=400)

        #判断两次密码是否一致
        if change_password != confirm_password:
            return Response({"errmsg": "两次密码不一致"}, status=400)

        #用于旧密码校验
        md5 = hashlib.md5()
        md5.update(local_password.encode())
        md5_passwd = md5.hexdigest()
        if md5_passwd !=user.password:
            return Response({"errmsg": "原密码输入错误"}, status=400)

        #用于新密码加密
        md5_new = hashlib.md5()
        md5_new.update(confirm_password.encode())
        new_password = md5_new.hexdigest()
        user.password = new_password
        try:
            user.save()
        except Exception as e:
            return Response({'errmsg':e},status=500)
        return Response({'data': "OK"})