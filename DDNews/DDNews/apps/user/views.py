from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,ListAPIView
from news.models import User_Fans,News,User,User_Collection
from rest_framework.response import Response

from .serializers import GetAuthor_Info_Serializer,Author_Fans, Author_Followed,User_Avatar_Url_Serializer,Get_UserNewsCollection_Serializer
#使用fastdfs 存储图片
from fdfs_client.client import Fdfs_client
import base64
from DDNews.utils.pagination import Newlist_Paginations
from rest_framework.filters import OrderingFilter

import hashlib



# 首页获取推荐作者
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


#用户新闻收藏的添加和取消
class UserNewCollection(APIView):
    def post(self,request):
        new_id = request.data.get('new_id')
        user =request.user
        try:
            new = News.objects.get(id=new_id)
        except:
            return Response({'errmsg':'参数错误'},status=400)

        #判断用户是有关注记录
        user_collection =  User_Collection.objects.filter(new_id=new_id,user=user).first()
        if user_collection:
            #更改关注信息
            user_collection.is_delete=False
            user_collection.save()
            return Response({'errmsg':'OK'})

        #用户与该新闻没有关注信息，创建集合
        User_Collection.objects.create(user=user,new=new)

        return Response({'errmsg':'OK'})

    def  delete(self,request):
        new_id = request.data.get('new_id')
        user = request.user

        try:
            #判断new_id信息是否正确
            News.objects.get(id=new_id)
        except:
            return Response({'errmsg':'参数错误'},status=400)

        # 判断用户是否未关注,只有关注才能删除
        user_collection = User_Collection.objects.filter(new_id=new_id, user=user).first()

        if not user_collection:
            return Response({'errmsg': '该新闻您未关注,请先关注'}, status=400)

        #标记删除
        user_collection.is_delete = True

        user_collection.save()

        return Response({'errmsg':'OK'})

#用户收藏新闻的获取
class GetUserNewsCollections(ListAPIView):
    serializer_class = Get_UserNewsCollection_Serializer
    pagination_class = Newlist_Paginations
    # 注册排序的使用
    filter_backends = [OrderingFilter]
    # 排序指定字段
    ordering = ['-create_time']

    def get_queryset(self):
        user = self.request.user

        return User_Collection.objects.filter(user=user,is_delete=False)

    # 去掉self.request可以让图片没有本地域名的前缀
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }


#查询新闻详情页否关注
class GetUserFollowAndCollection(APIView):
    def get(self,request,pk):
        new_id =pk
        try:
            new = News.objects.get(id=new_id)
        except:
            return Response({'errmsg':'参数错误'},status=400)

        # 通过新闻id获取作者id
        author_id = new.user_id

        user = request.user
        user_id = user.id

        data = {}

        #查询用户是否收藏
        user_collection= User_Collection.objects.filter(user=user,new_id=new_id,is_delete=False)
        if not user_collection:
            data['collection'] = 'false'
        else:
            data['collection'] = 'true'

        #查询用户是否存在关注关系
        try:
            user_fan = User_Fans.objects.filter(follow_id=author_id,fan_id=user_id)
        except:
            return Response({'errmsg':'查询数据失败'},status=400)

        if not user_fan:
            data['follow'] = 'false'
        else:
            data['follow'] = 'true'

        return Response({'data':data})


# 作者中心页的关注信息　通过author_id是否关注
class GetUserfollow(APIView):
    def get(self, request, pk):

        author_id = pk

        try:
            User.objects.get(id=author_id)
        except:
            return Response({'errmsg':'参数错误'},status=400)

        user = request.user
        user_id = user.id
        try:
            user_fan = User_Fans.objects.filter(follow_id=author_id, fan_id=user_id)
        except:
            return Response({'errmsg': '查询数据失败'},status=400)

        if not user_fan:
            return Response({'data': 'false'})
        return Response({'data': 'true'})


#关注与取消关注
class User_Followed(APIView):
    def post(self,request):
        author_id = request.data.get('author_id')
        user = self.request.user

        if user.id == int(author_id):
            return Response({"errmsg":"自己不能关注自己"},status=400)

        try:
            author = User.objects.get(id=author_id)
        except:
            return Response({'errmsg':'获取作者信息失败'},status=400)

        if not author:
            return Response({'errmsg':'作者不存在'},status=400)


        User_Fans.objects.create(fan=user,follow=author)


        return Response({'errmsg':'OK'})


    def delete(self,request):
        author_id = request.data.get('author_id')
        user = self.request.user

        try:
            author = User.objects.get(id=author_id)
        except:
            return Response({'errmsg':'获取作者信息失败'},status=400)

        if not author:
            return Response({'errmsg':'作者不存在'},status=400)


        user_fans = User_Fans.objects.filter(fan=user, follow=author).first()
        if not user_fans:
            return Response({'errmsg':'参数错误'},status=400)

        user_fans.delete()
        return Response({'errmsg':'OK'})

#获取作者信息
class GetAuthor_Info(RetrieveAPIView):
    serializer_class = GetAuthor_Info_Serializer
    def get_object(self):
        pk = self.kwargs['pk']
        try:
            User.objects.get(id=pk)
        except:
            return Response({'errmsg':'参数错误'},status=400)

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
    pagination_class = Newlist_Paginations
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
            return Response({"errmsg":"用户数据错误"},status=400)
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
            return Response({'errmsg':'保存失败'},status=400)

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


#用户头像上传
class UploadUserAvatar(APIView):

    # serializer_class = User_Avatar_Url_Serializer
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     try:
    #         user = User.objects.get(id=pk)
    #     except:
    #         return Response({"errmsg": "用户数据错误"}, status=400)
    #     return user
    #
    def put(self,request,pk):
        user_id = pk
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"errmsg": "用户数据错误"}, status=400)
        user_avatar = request.data.get('avatar')


        #客户端链接实例
        client = Fdfs_client('DDNews/utils/fastdfs/client.conf')
        #保存读取传来的数据
        image_ = user_avatar.read()

        # print(type(img_info))
        print(type(image_))

        # with open('./zz.jpg','wb')as f:
        #     f.write(image_)

        ret = client.upload_by_buffer(image_)

        print(ret['Remote file_id'])
        user.avatar_url = "http://192.168.72.128:8888/"+ret['Remote file_id']
        user.save()

        return Response({"avatar_url":user.avatar_url,'errmsg':'保存成功'})