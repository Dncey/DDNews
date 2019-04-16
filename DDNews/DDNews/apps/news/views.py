from django.shortcuts import render
from news.models import NewsCategory,News,Slide_image,Search_keywords
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import Get_Newslist_Serializer,New_Detail_Serializer
from DDNews.utils.pagination import Newlist_Paginations
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

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

#新闻列表数据，分页，过滤排序功能
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
            return News.objects.all()
        else:
            return News.objects.filter(category=pk)

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
        #审核状态通过
        return News.objects.filter(id=pk,status=0).first()