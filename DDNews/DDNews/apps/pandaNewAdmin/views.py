from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from news.models import News,NewsCategory
from django.db.models import Count
from DDNews.utils.pagination import Newlist_Paginations
from .serializers import All_author_Get_Newslist_Serializer
from news.models import User
import hashlib
import time
from datetime import datetime, timedelta

# import datetime
# from news.models import User
# import random
#管理员登录
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
        #插入随机用户
        # now = datetime.datetime.now()
        # for num in range(0, 1000):
        #     try:
        #         user = User()
        #         user.username = "%011d" % num
        #         user.mobile = "%011d" % num
        #         user.password = "e10adc3949ba59abbe56e057f20f883e"
        #         user.last_login = now - datetime.timedelta(seconds=random.randint(0, 2678400))
        #         user.save()
        #         print(user.mobile)
        #     except Exception as e:
        #         print(e)

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


#用户数据统计
class User_Day_Active(APIView):
    def get(self,request):
        #查询搜索用户人数
        total_count = User.objects.filter(is_superuser=0).count()
        #查询月新增人数

        now = time.localtime()
        now_begin = '%d-%02d-01'%(now.tm_year,now.tm_mon)
        now_begin_date = datetime.strptime(now_begin,'%Y-%m-%d')
        mon_count = User.objects.filter(is_superuser=0,date_joined__gte=now_begin_date).count()

        #日新增人数
        day_begin = '%d-%02d-%02d' %(now.tm_year,now.tm_mon,now.tm_mday)
        day_begin_date = datetime.strptime(day_begin,'%Y-%m-%d')
        day_count = User.objects.filter(is_superuser=0,date_joined__gte=day_begin_date).count()

        #查询图标信息
        #获取到当天00:00:00时间
        now_date=datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
        active_date = []
        active_count = []
        #依次添加数据，再反转
        for i in range(0,31):
            begin_date = now_date-timedelta(days=i)
            end_date = now_date-timedelta(days=(i-1))
            active_date.append(begin_date.strftime('%Y-%m-%d'))

            user_count = User.objects.filter(is_superuser=0,last_login__gte=begin_date,last_login__lt=end_date).count()
            active_count.append(user_count)

        active_count.reverse()
        active_date.reverse()

        data={
            "total_count":total_count,
            "mon_count":mon_count,
            "day_count":day_count,
            "active_date":active_date,
            "active_count":active_count
        }
        return Response(data)


#新闻数据统计

class News_Detail_Analysis(APIView):
    def get(self,request):

        #-------获取用户-作者分布
        #查询所有用户发布的新闻个数
        author = News.objects.all().values('user_id').annotate(count=Count('user_id'))
        #获取作者的数量
        author_count = author.count()
        #所有用户的数量
        all_user = User.objects.filter(is_superuser=0).count()
        #所有用户减去作者即为用户数量
        user_count = all_user - author_count
        #用字典保存用户－作者分布图数据
        author_user = {}
        author_user['author_count']=author_count
        author_user['user_count']=user_count

        #------获取当前新闻分类数量
        new_category = News.objects.all().values('category').annotate(count=Count('category_id'))

        #遍历查到的分类ｉｄ,把分类id替换成分类名字
        for x in new_category:
            x['category'] = NewsCategory.objects.get(id=x['category']).name

        #-------周作者新闻发布排行

        # 获取到当天00:00:00时间
        now_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')

        #获取七天前的日期
        begin_date = now_date - timedelta(days=6)
        print(begin_date.strftime('%Y-%m-%d'))
        #获取新闻上传日期是７天前到今天新闻的作者的数量
        wekkend_order_author = News.objects.filter(create_time__gte=begin_date).all().values('user_id').annotate(count=Count('user_id'))

        #把用户id换成用户姓名
        for y in wekkend_order_author:
            y['user_id']=User.objects.get(id=y['user_id']).username

        #--------获取一周内各分类新闻的发布量






        data = {
            'author_user':author_user,
            'new_category':new_category,
            'wekkend_order_author':wekkend_order_author,
        }
        return Response(data)




#所有作者新闻获取
class AllAuthor_Newlist(ListAPIView):
    serializer_class = All_author_Get_Newslist_Serializer
    pagination_class = Newlist_Paginations
    # 注册排序的使用
    filter_backends = [OrderingFilter]
    filter_fields = ('status')
    # 排序指定字段
    ordering = ['report_time','status']

    def get_queryset(self):
        return News.objects.all()

#作者新闻审核
class Author_New_Review(APIView):
    def get(self,request,pk):
        new_id = pk
        user = request.user
        #查询是否是管理员
        user=User.objects.filter(id=user.id,is_superuser=1).filter().first()
        if not user:
            return Response({'errmsg':'用户错误'},status=400)
        try:
            new = News.objects.get(id=new_id)
        except:
            return Response({'errmsg':'数据错误'})

        if not new:
            return Response({'errmsg': '参数错误'}, status=400)

        data = {}
        data['title'] = new.title
        data['category_id'] = new.category_id
        data['digest'] = new.digest
        data['content'] = new.content
        return Response({"data": data})

    def put(self,request,pk):
        new_id = pk
        title = request.data.get("title")
        category_id = request.data.get("category_id")
        digest = request.data.get("digest")
        content = request.data.get("content")
        review_status = request.data.get("review_status")
        reason = request.data.get("reason")
        user = request.user
        # 查询是否是管理员
        user = User.objects.filter(id=user.id, is_superuser=1).filter().first()
        if not user:
            return Response({'errmsg': '用户错误'}, status=400)

        try:
            new = News.objects.get(id=new_id)
        except:
            return Response({'errmsg': '数据错误'})

        if not new:
            return Response({'errmsg': '参数错误'}, status=400)

        #判断选择的审核状态
        if review_status =='reject':
            new.reason =reason
            new.status=2
        elif review_status =='accept':
            new.status=0
        else:
            new.status=1

        new.title = title
        new.category_id=category_id
        new.digest = digest
        new.content =content
        new.save()
        return Response({'errmsg':'保存成功'})
