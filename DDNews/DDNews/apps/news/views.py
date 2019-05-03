
from django.db.models import Q
from django.shortcuts import render
from news.models import NewsCategory,News,Slide_image,Search_keywords,Comment
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import Get_Newslist_Serializer,New_Detail_Serializer, New_Add_Comment_Serializer,New_Get_Comment_Serializer,GetGoodNewsSerializer,Author_News_Status_Serializer
from DDNews.utils.pagination import Newlist_Paginations
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
#使用fastdfs 存储图片
from fdfs_client.client import Fdfs_client
import re
import jieba
from jieba import analyse
import datetime

#获取菜单列表
class Category_info(APIView):
    def get(self,request):

        categorys_list = []
        categorys = NewsCategory.objects.all()
        for category in categorys[0:9]:
            dict = {}
            dict['id'] = category.id
            dict['name'] = category.name
            categorys_list.append(dict)

        context = {
            'errmsg':'OK',
            'data':categorys_list
        }
        return Response(context)

#获取首页轮播图信息
class Get_Slideshow_Apiview(APIView):
    def get(self,request):
        try:
            slide_shows = Slide_image.objects.filter(is_recommend=True)[0:3]
        except:
            return Response({'errmsg':'查询数据库错误'})
        slide_show_list = []
        for slide_show in slide_shows:
            dict = {}
            dict['title'] = slide_show.title
            dict['new_id'] =slide_show.new_id
            dict['image_url'] = slide_show.url
            slide_show_list.append(dict)
        data = {
            'data':slide_show_list
        }
        return Response(data)

#获取搜索关键字
class Get_Search_Keyswords(APIView):
    def get(self,request):
        search_keywords = Search_keywords.objects.order_by('-search_times').all()[:8]
        search_keyword_list = []
        for search_keyword in search_keywords:

            search_keyword_list.append(search_keyword.key_wrods)
        data = {
            'errmsg':'OK',
            'data':search_keyword_list
        }

        return Response(data)


#获取精选新闻
class GetGoodNews(APIView):

    def get(self,request):
        news = News.objects.filter(status=0).order_by('-clicks').all()[:6]
        serializer = GetGoodNewsSerializer(news,many=True)


        return Response(serializer.data)

#首页新闻列表数据，分页，过滤排序功能
class Get_Newslist_ListApiView(ListAPIView):
    serializer_class = Get_Newslist_Serializer
    pagination_class = Newlist_Paginations
    #注册排序的使用
    filter_backends = [OrderingFilter]
    #排序指定字段
    ordering = ['report_time']
    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk == '0' :
            return News.objects.filter(status=0).all()
        else:
            return News.objects.filter(category=pk,status=0)

    #去掉self.request可以让图片没有本地域名的前缀
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }


#新闻详情页数据的获取,添加修改，删除
class New_Detail_ViewSet(ModelViewSet):
    serializer_class = New_Detail_Serializer
    def get_object(self):
        pk = self.kwargs["pk"]
        new = News.objects.filter(id=pk, status=0).first()
        new.clicks += 1
        new.save()
        #审核状态通过
        return new


#新闻评论
class New_Comment(ListAPIView,CreateAPIView):
    pagination_class = Newlist_Paginations
    def get_serializer_class(self):
        # print(self.request.method)
        if self.request.method == 'POST':
            return New_Add_Comment_Serializer
        if self.request.method == 'GET':
            return New_Get_Comment_Serializer

    def get_queryset(self):
        new_id = self.request.query_params.get('new_id')
        all_comment = Comment.objects.filter(new_id=new_id, parent_id__isnull=True).all().order_by('-create_time')
        return all_comment

    def list(self, request, *args, **kwargs):

        #先通过new_id查询所有的评论
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


#作者新闻页新闻获取
class Author_Newlist(ListAPIView):
    serializer_class = Get_Newslist_Serializer
    pagination_class = Newlist_Paginations
    # 注册排序的使用
    filter_backends = [OrderingFilter]
    # 排序指定字段
    ordering = ['report_time']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return News.objects.filter(user_id=pk,status=0)

    # 去掉self.request可以让图片没有本地域名的前缀
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }


#搜索新闻
class NewsSearchView(ListAPIView):

    def get_queryset(self):

        pk= self.request.query_params.get('keywords')
        return News.objects.filter(Q(title__contains=pk)|Q(digest_label__contains=pk),status=0).order_by("-report_time")

    serializer_class = Get_Newslist_Serializer
    pagination_class = Newlist_Paginations

    # 去掉self.request可以让图片没有本地域名的前缀
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }


#新闻图片内容上传
class NewsImageUpload(APIView):
    def post(self,request):
        new_image = request.data.get('new_image')
        if not new_image:
            return Response({'errmsg':'无图片数据','errno':2},status=400)

        # 客户端链接实例
        client = Fdfs_client('DDNews/utils/fastdfs/client.conf')
        # 保存读取传来的数据
        image_ =new_image.read()
        ret = client.upload_by_buffer(image_)
        image_url = "http://192.168.72.128:8888/"+ret['Remote file_id']

        return Response({'errno':0,"url":image_url})


#新闻内容上传
class NewContent_upload(APIView):
    def post(self,request):
        title =request.data.get('title')
        category_id =request.data.get('category_id')
        digest =request.data.get('digest')

        try:
            NewsCategory.objects.get(id=category_id)
        except:
            return Response({'errmsg':"参数错误"},status=400)

        #带标签的新闻内容
        content =request.data.get('content')

        #纯文本内容
        text = request.data.get('text')
        user = request.user
        if not all([title,content,category_id]):
            return Response({'errmsg':"参数缺失"},status=400)

        #如果文章简要为空，则默认为标题
        if not digest:
            digest = text[:80]

        # 匹配出文章中的图片
        img_reg = re.compile(r'.*?img src="((?:http|https|//).*?)"')
        # 文章的图片所有url
        image_urls = img_reg.findall(content)

        #判断文章是否有图片
        if not image_urls:
            index_url = ''
        else:
            index_url = image_urls[0]
            image_urls = str(image_urls[:3])


        # content_reg = re.compile(r'([\u4E00-\u9FA5]+)') 匹配中文


        #使用jieba提取文章关键字
        tags = jieba.analyse.extract_tags(text, topK=5)  # 采用jieba.analyse.extrack_tags(content, topK)提取关键词
        #转换字符串存储数据库中

        print(tags)

        News.objects.create(title=title,source=user.username,index_image_url=index_url,index_image_url_list=image_urls,digest=digest,content=content,status=1,digest_label=tags,is_spider=False,source_avatar_url=user.avatar_url,report_time=datetime.datetime.now(),category_id=category_id,user=user)

        return Response({'errno':"OK"})


#获取作者上传新闻状态
class Author_News_Status(ListAPIView):

    serializer_class = Author_News_Status_Serializer
    pagination_class = Newlist_Paginations
    # 注册排序的使用
    filter_backends = [OrderingFilter]
    # 排序指定字段
    ordering = ['report_time']

    def get_queryset(self):
        user= self.request.user
        return News.objects.filter(user=user)


#更新修改新闻
class Author_News_Update(APIView):
    def get(self,request,pk):
        user = request.user

        new_id = pk

        new = News.objects.filter(user=user,id=new_id).first()

        if not new:
            return Response({'errmsg':'参数错误'})

        data = {}
        data['title'] = new.title
        data['category_id'] = new.category_id
        data['digest'] = new.digest
        data['content'] = new.content


        return Response({"data":data})


    def put(self,request,pk):
        pass