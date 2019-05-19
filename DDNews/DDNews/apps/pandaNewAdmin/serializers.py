from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from news.models import News,Slide_image



#审核页面所有作者新闻
class All_author_Get_Newslist_Serializer(ModelSerializer):
    report_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = News
        fields = ('id','title','report_time','status')


#新闻轮播图管理
class Slide_image_Serializer(ModelSerializer):

    class Meta:
        model = Slide_image
        fields = ('new_id','title','url','is_recommend')